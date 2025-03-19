#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 19-mar-2025
Purpose: Try get_latest_episodes in AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

__all__ = ["get_latest_episodes"]

import argparse
import re
from typing import List, Union
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ..config import BASE_URL
from ..models import EpisodeInfo
from ..utils import AnimeFLVParseError
from .connect import AnimeFLV


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""Fetches the latest episodes from AnimeFLV.

            This script retrieves a list of the most recent episodes
            (possibly this last week) from AnimeFLV.

            Example usage:
                python -m src.api.handlers.get_latest_episodes
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    return parser.parse_args()


# --------------------------------------------------
def get_latest_episodes(animeflv: AnimeFLV = None) -> List[EpisodeInfo]:
    """
    Retrieves a list of new episodes released on AnimeFLV.

    This function fetches the latest episodes from AnimeFLV and returns a list of EpisodeInfo objects.
    The episodes are possibly from the last week.

    Args:
        animeflv (AnimeFLV, optional): An instance of AnimeFLV. Defaults to None.

    Returns:
        List[EpisodeInfo]: A list of EpisodeInfo objects representing the latest episodes.
    """

    if animeflv is None:
        animeflv = AnimeFLV()

    response = animeflv._scraper.get(BASE_URL)
    soup = BeautifulSoup(response.text, "lxml")

    elements = soup.select("ul.ListEpisodios li a")
    ret = []

    for element in elements:
        try:
            anime, _, id = element["href"].rpartition("-")

            ret.append(
                EpisodeInfo(
                    id=id,
                    anime=removeprefix(anime, "/ver/"),
                    image_preview=f"{BASE_URL}{element.select_one('span.Image img').get('src')}",
                )
            )
        except Exception as exc:
            raise AnimeFLVParseError(exc)

    return ret


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    with AnimeFLV() as api:
        try:
            results = get_latest_episodes(animeflv=api)
            for result in results:
                print(f"{result.id} - {result.anime}")
        except Exception as e:
            print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.get_latest_episodes

