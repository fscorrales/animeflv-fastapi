#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 19-mar-2025
Purpose: Try get_latest_animes in AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

__all__ = ["get_latest_animes"]

import argparse
import re
from typing import List, Union
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ..config import BASE_URL
from ..models import AnimeInfo
from ..utils import AnimeFLVParseError, process_anime_list_info
from .connect import AnimeFLV


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""Fetches the latest anime releases from AnimeFLV.

            This script retrieves a list of the most recent anime releases
            from AnimeFLV.

            Example usage:
                python -m src.api.handlers.get_latest_animes
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    return parser.parse_args()


# --------------------------------------------------
def get_latest_animes(animeflv: AnimeFLV = None) -> List[AnimeInfo]:
    """
    Retrieves a list of new anime releases from AnimeFLV.

    This function fetches the latest anime releases from AnimeFLV and returns a list of AnimeInfo objects.

    Args:
        animeflv (AnimeFLV, optional): An instance of AnimeFLV. Defaults to None.

    Returns:
        List[AnimeInfo]: A list of AnimeInfo objects representing the latest anime releases.

    Raises:
        AnimeFLVParseError: If the parsing of the AnimeFLV page fails.
    """

    if animeflv is None:
        animeflv = AnimeFLV()

    response = animeflv._scraper.get(BASE_URL)
    soup = BeautifulSoup(response.text, "lxml")

    elements = soup.select("ul.ListAnimes li article")

    if elements is None:
        raise AnimeFLVParseError("Unable to get list of animes")

    return process_anime_list_info(elements)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    with AnimeFLV() as api:
        try:
            results = get_latest_animes(animeflv=api)
            for result in results:
                print(f"{result.id} - Title: {result.title} - Synopsis: {result.synopsis}")
        except Exception as e:
            print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.get_latest_animes

