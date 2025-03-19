#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 18-mar-2025
Purpose: Try search in AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

__all__ = ["search"]

import argparse
from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from ..config import BROWSE_URL
from ..models import AnimeInfo
from ..utils import AnimeFLVParseError, process_anime_list_info, wrap_request
from .connect import AnimeFLV


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""Busca animes en la API de AnimeFLV.

            Este script toma un término de búsqueda como entrada y devuelve una lista
            de animes que coinciden con el término de búsqueda.

            Example usage:
                python -m src.api.handlers.search_anime one-piece
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
        try:
            elements = wrap_request(lambda: search(args.title, animeflv=api))
            for i, element in enumerate(elements):
                print(f"{i}, id: {element.id}, title: {element.title}")
        except Exception as e:
            print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.search_anime "Dragon Ball Z"
    # python -m src.api.handlers.search_anime "One Piece"
