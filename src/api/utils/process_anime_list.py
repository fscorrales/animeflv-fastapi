__all__ = ["process_anime_list_info"]

from typing import List

from bs4 import ResultSet

from ..models import AnimeInfo
from .exceptions import AnimeFLVParseError
from .remove_prefix import removeprefix


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
                        element.select_one("a div.Image figure img").get("src", None)
                        or element.select_one("a div.Image figure img")["data-cfsrc"]
                    ),
                    banner=(
                        element.select_one("a div.Image figure img").get("src", None)
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
