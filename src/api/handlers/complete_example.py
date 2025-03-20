#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gamail.com>
Date   : 20-mar-2025
Purpose: Try most handlers at once
Source : https://github.com/jorgeajimenezl/animeflv-api
Idea   : https://www.youtube.com/shorts/7uZL7idkqJ0?si=GhxmCY67Kfk4nRAi
"""

import argparse

from ..utils import wrap_request
from . import AnimeFLV, get_anime_info, get_links, search


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Demonstrate the usage of multiple AnimeFLV handlers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    with AnimeFLV() as api:
        try:
            # elements = api.search(input("Serie to search: "))
            serie = input("Serie to search: ")
            elements = wrap_request(lambda: search(serie, animeflv=api))
            for i, element in enumerate(elements):
                print(f"{i}, id: {element.id}, title: {element.title}")
            selection = int(input("Select option: "))
            serie = elements[selection].id
            # info = api.get_anime_info(elements[selection])
            info = wrap_request(lambda: get_anime_info(serie, animeflv=api))
            print(f"Título: {info.title}")
            print(f"Sinopsis: {info.synopsis}")
            print(f"Tipo: {info.type}")
            generos_string = ", ".join(info.genres)
            print(f"Generos: {generos_string}")
            print(f"Debut: {info.debut}")
            print(f"Rating: {info.rating}")
            info.episodes.reverse()
            for j, episode in enumerate(info.episodes):
                print(f"{j}, | Episode - {episode.id}")
            index_episode = int(input("Select episode: "))
            capitulo = info.episodes[index_episode].id
            # results = api.get_links(serie, capitulo)
            results = wrap_request(lambda: get_links(serie, capitulo, animeflv=api))
            for result in results:
                print(f"{result.server} - {result.url}")
        except Exception as e:
            print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.complete_example
