#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 18-mar-2025
Purpose: Try AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

import argparse
from ..models import AnimeInfo
from ..config import BROWSE_URL
from bs4 import BeautifulSoup, ResultSet
from urllib.parse import urlencode
from typing import List
from .connect import AnimeFLV
from ..utils import AnimeFLVParseError

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Try AnimeFlv API',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    return parser.parse_args()

# --------------------------------------------------
def process_anime_list_info(elements: ResultSet) -> List[AnimeInfo]:
    ret = []

    for element in elements:
        try:
            ret.append(
                AnimeInfo(
                    id=removeprefix(
                        element.select_one("div.Description a.Button")["href"][1:],
                        "anime/",
                    ),
                    title=element.select_one("a h3").string,
                    poster=(
                        element.select_one("a div.Image figure img").get(
                            "src", None
                        )
                        or element.select_one("a div.Image figure img")["data-cfsrc"]
                    ),
                    banner=(
                        element.select_one("a div.Image figure img").get(
                            "src", None
                        )
                        or element.select_one("a div.Image figure img")["data-cfsrc"]
                    )
                    .replace("covers", "banners")
                    .strip(),
                    type=element.select_one("div.Description p span.Type").string,
                    synopsis=(
                        element.select("div.Description p")[1].string.strip()
                        if element.select("div.Description p")[1].string
                        else None
                    ),
                    rating=element.select_one("div.Description p span.Vts").string,
                    debut=(
                        element.select_one("a span.Estreno").string.lower()
                        if element.select_one("a span.Estreno")
                        else None
                    ),
                )
            )
        except Exception as exc:
            raise AnimeFLVParseError(exc)

    return ret

# --------------------------------------------------
def search(query: str = None, page: int = None, animeflv: AnimeFLV = None) -> List[AnimeInfo]:
    """
    Search in animeflv.net by query.
    :param query: Query information like: 'Nanatsu no Taizai'.
    :param page: Page of the information return.
    :rtype: list[AnimeInfo]
    """

    if animeflv is None:
        animeflv = AnimeFLV()

    if page is not None and not isinstance(page, int):
        raise TypeError

    params = dict()
    if query is not None:
        params["q"] = query
    if page is not None:
        params["page"] = page
    params = urlencode(params)

    url = f"{BROWSE_URL}"
    if params != "":
        url += f"?{params}"

    response = animeflv._scraper.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    elements = soup.select("div.Container ul.ListAnimes li article")

    if elements is None:
        raise AnimeFLVParseError("Unable to get list of animes")

    return process_anime_list_info(elements)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    # args = get_args()

    with AnimeFLV() as api:
        elements = search(input('Serie to search: '), animeflv=api)
        for i, element in enumerate(elements):
            print(f'{i}, {element.title} - {element.url}')
        # try:
        #     selection = int(input('Select option: '))
        #     info = api.get_anime_info(elements[selection])
        #     info.episodes.reverse()
        #     for j, episode in enumerate(info.episodes):
        #         print(f'{j}, | Episode - {episode.id} - {episode.url}')
        #     index_episode = int(input('Select episode: '))
        #     serie = elements[selection].id
        #     capitulo = info.episodes[index_episode].id
        #     results = api.get_links(serie, capitulo)
        #     for result in results:
        #         print(f"{result.server} - {result.url}")
        # except Exception as e:
        #     print(e)
        

# --------------------------------------------------
if __name__ == '__main__':
    main()

    # python -m src.api.handlers.search