#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 18-mar-2025
Purpose: Try get_links in AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

__all__ = ["get_links"]

import argparse
import re
from typing import List, Union
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ..config import ANIME_VIDEO_URL
from ..models import DownloadLinkInfo, EpisodeFormat
from ..utils import AnimeFLVParseError, parse_table
from .connect import AnimeFLV


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""
            Retrieves download links for a specific anime episode from AnimeFLV.

            This script takes an anime ID and an episode number as input, 
            and returns a list of download links for that episode.

            Example usage:
                python -m src.api.handlers.get_anime_links one-piece-tv -e 10
                python -m src.api.handlers.get_anime_links dragon-ball-z -e 5
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

    parser.add_argument(
        "-e",
        "--episode",
        help="Episode id, like as '1'",
        metavar="int",
        type=int,
        default=1,
    )

    return parser.parse_args()


# --------------------------------------------------
def get_links(
    id: str,
    episode: Union[str, int],
    format: EpisodeFormat = EpisodeFormat.Subtitled,
    animeflv: AnimeFLV = None,
    **kwargs,
) -> List[DownloadLinkInfo]:
    """
    Get download links of specific episode.
    Return a list of dictionaries like:
    [
        {
            "server": "...",
            "url": "..."
        },
        ...
    ]

    :param id: Anime id, like as 'nanatsu-no-taizai'.
    :param episode: Episode id, like as '1'.
    :param **kwargs: Optional arguments for filter output (see doc).
    :rtype: list
    """

    if animeflv is None:
        animeflv = AnimeFLV()

    response = animeflv._scraper.get(f"{ANIME_VIDEO_URL}{id}-{episode}")
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", attrs={"class": "RTbl"})

    try:
        rows = parse_table(table)
        ret = []

        for row in rows:
            if (
                row["FORMATO"].string == "SUB"
                and EpisodeFormat.Subtitled in format
                or row["FORMATO"].string == "LAT"
                and EpisodeFormat.Dubbed in format
            ):
                ret.append(
                    DownloadLinkInfo(
                        server=row["SERVIDOR"].string,
                        url=re.sub(
                            r"^http[s]?://ouo.io/[A-Za-z0-9]+/[A-Za-z0-9]+\?[A-Za-z0-9]+=",
                            "",
                            unquote(row["DESCARGAR"].a["href"]),
                        ),
                    )
                )

        return ret
    except Exception as exc:
        raise AnimeFLVParseError(exc)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    with AnimeFLV() as api:
        try:
            results = get_links(args.anime_id, str(args.episode), animeflv=api)
            for result in results:
                print(f"{result.server} - {result.url}")
        except Exception as e:
            print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.get_anime_links one-piece-tv -e 10
    # python -m src.api.handlers.get_anime_links dragon-ball-z
