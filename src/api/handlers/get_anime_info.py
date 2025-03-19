#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 18-mar-2025
Purpose: Try get_anime_info in AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

__all__ = ["get_anime_info"]

import argparse
import json

from bs4 import BeautifulSoup

from ..config import ANIME_URL, BASE_EPISODE_IMG_URL, BASE_URL
from ..models import AnimeInfo, EpisodeInfo
from ..utils import AnimeFLVParseError, wrap_request
from .connect import AnimeFLV


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""Fetches information about a specific anime from the AnimeFLV API.

            This script retrieves information about an anime, including title, description, genres, and episodes.

            Example usage:
                python -m src.api.handlers.get_anime_info one-piece-tv
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "anime_id",
        metavar="str",
        help="Anime's id to look up like as 'nanatsu-no-taizai'",
        type=str,
        default="",
    )

    return parser.parse_args()


# --------------------------------------------------
def get_anime_info(id: str, animeflv: AnimeFLV) -> AnimeInfo:
    """
    Retrieves information about a specific anime from the AnimeFLV API.

    This function fetches information about an anime, including title, description, genres, and episodes.

    Args:
        anime_id (str): The ID of the anime to retrieve information about.
        animeflv (AnimeFLV, optional): An instance of AnimeFLV. Defaults to None.

    Returns:
        AnimeInfo: An AnimeInfo object containing information about the anime.

    Raises:
        AnimeFLVParseError: If the parsing of the AnimeFLV page fails.
    """

    if animeflv is None:
        animeflv = AnimeFLV()

    response = animeflv._scraper.get(f"{ANIME_URL}/{id}")
    soup = BeautifulSoup(response.text, "lxml")

    synopsis = soup.select_one(
        "body div div div div div main section div.Description p"
    ).string

    information = {
        "title": soup.select_one(
            "body div.Wrapper div.Body div div.Ficha.fchlt div.Container h1.Title"
        ).string,
        "poster": BASE_URL
        + "/"
        + soup.select_one(
            "body div div div div div aside div.AnimeCover div.Image figure img"
        ).get("src", ""),
        "synopsis": synopsis.strip() if synopsis else None,
        "rating": soup.select_one(
            "body div div div.Ficha.fchlt div.Container div.vtshr div.Votes span#votes_prmd"
        ).string,
        "debut": soup.select_one(
            "body div.Wrapper div.Body div div.Container div.BX.Row.BFluid.Sp20 aside.SidebarA.BFixed p.AnmStts"
        ).string,
        "type": soup.select_one(
            "body div.Wrapper div.Body div div.Ficha.fchlt div.Container span.Type"
        ).string,
    }
    information["banner"] = information["poster"].replace("covers", "banners").strip()
    genres = []

    for element in soup.select("main.Main section.WdgtCn nav.Nvgnrs a"):
        if "=" in element["href"]:
            genres.append(element["href"].split("=")[1])

    info_ids = []
    episodes_data = []
    episodes = []

    try:
        for script in soup.find_all("script"):
            contents = str(script)

            if "var anime_info = [" in contents:
                anime_info = contents.split("var anime_info = ")[1].split(";")[0]
                info_ids.append(json.loads(anime_info))

            if "var episodes = [" in contents:
                data = contents.split("var episodes = ")[1].split(";")[0]
                episodes_data.extend(json.loads(data))

        AnimeThumbnailsId = info_ids[0][0]
        # animeId = info_ids[0][2]
        # nextEpisodeDate = info_ids[0][3] if len(info_ids[0]) > 4 else None

        for episode, _ in episodes_data:
            episodes.append(
                EpisodeInfo(
                    id=episode,
                    anime=id,
                    image_preview=f"{BASE_EPISODE_IMG_URL}{AnimeThumbnailsId}/{episode}/th_3.jpg",
                )
            )

    except Exception as exc:
        raise AnimeFLVParseError(exc)

    return AnimeInfo(
        id=id,
        episodes=episodes,
        genres=genres,
        **information,
    )


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    with AnimeFLV() as api:
        try:
            anime = wrap_request(lambda: get_anime_info(args.anime_id, animeflv=api))
            print(f"Título: {anime.title}")
            print(f"Sinopsis: {anime.synopsis}")
            print(f"Tipo: {anime.type}")
            generos_string = ", ".join(anime.genres)
            print(f"Generos: {generos_string}")
            print(f"Debut: {anime.debut}")
            print(f"Rating: {anime.rating}")
            anime.episodes.reverse()
            for j, episode in enumerate(anime.episodes):
                print(f"{j}, | Episode - {episode.id}")
        except Exception as e:
            print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.get_anime_info one-piece-tv
    # python -m src.api.handlers.get_anime_info dragon-ball-z
