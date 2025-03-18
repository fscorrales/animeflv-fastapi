#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 18-mar-2025
Purpose: Try search in AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

import argparse
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from ..config import BROWSE_URL
from ..models import AnimeInfo
from ..utils import AnimeFLVParseError, process_anime_list_info
from .connect import AnimeFLV


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""
        Función de búsqueda para la API de AnimeFlv. 
        Permite buscar series de anime en el sitio web de AnimeFlv y devuelve 
        los resultados en forma de lista de elementos
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "title", metavar="str", help="Anime's title to search", type=str, default=""
    )

    return parser.parse_args()


# --------------------------------------------------
def search(
    query: str = None, page: int = None, animeflv: AnimeFLV = None
) -> List[AnimeInfo]:
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

    args = get_args()

    with AnimeFLV() as api:
        elements = search(args.title, animeflv=api)
        for i, element in enumerate(elements):
            print(f"{i}, {element.title}")
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
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.search
