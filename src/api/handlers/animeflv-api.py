#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gamail.com>
Date   : 17-mar-2025
Purpose: Try AnimeFlv API
Source : https://github.com/jorgeajimenezl/animeflv-api
Youtube: https://www.youtube.com/shorts/7uZL7idkqJ0?si=GhxmCY67Kfk4nRAi
"""

import argparse

from animeflv import AnimeFLV


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Try AnimeFlv API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    # args = get_args()

    with AnimeFLV() as api:
        elements = api.search(input("Serie to search: "))
        for i, element in enumerate(elements):
            print(f"{i}, {element.title}")
        try:
            selection = int(input("Select option: "))
            info = api.get_anime_info(elements[selection])
            info.episodes.reverse()
            for j, episode in enumerate(info.episodes):
                print(f"{j}, | Episode - {episode.id} - {episode.url}")
            index_episode = int(input("Select episode: "))
            serie = elements[selection].id
            capitulo = info.episodes[index_episode].id
            results = api.get_links(serie, capitulo)
            for result in results:
                print(f"{result.server} - {result.url}")
        except Exception as e:
            print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.handlers.animeflv-api
