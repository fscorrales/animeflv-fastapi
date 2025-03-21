__all__ = ["AnimeFLVService", "AnimeFLVServiceDependency"]

from typing import Annotated, List

from fastapi import Depends

from ..config import logger
from ..handlers import get_latest_animes, get_latest_episodes, search, get_anime_info, get_anime_links
from ..models import EpisodeInfo, BaseAnimeInfo, FullAnimeInfo, DownloadLinkInfo
from ..utils import wrap_request


class AnimeFLVService:
    @classmethod
    def get_latest_animes(cls) -> List[BaseAnimeInfo]:
        try:
            anime_list = []
            results = wrap_request(lambda: get_latest_animes())
            for result in results:
                anime_list.append(
                    BaseAnimeInfo(
                        id=result.id,
                        title=result.title,
                        synopsis=result.synopsis,
                        poster=result.poster,
                        type=result.type,
                        rating=result.rating,
                        debut=result.debut,
                    )
                )
        except Exception as e:
            logger.error(f"Error during getting latest animes: {e}")

        return anime_list

    @classmethod
    def get_latest_episodes(cls) -> List[EpisodeInfo]:
        try:
            episodes_list = []
            results = wrap_request(lambda: get_latest_episodes())
            for result in results:
                episodes_list.append(
                    EpisodeInfo(
                        id=result.id,
                        anime=result.anime,
                        image_preview=result.image_preview,
                    )
                )
        except Exception as e:
            logger.error(f"Error during getting latest episodes: {e}")

        return episodes_list

    @classmethod
    def search_anime(cls, title: str) -> List[BaseAnimeInfo]:
        try:
            anime_list = []
            results = wrap_request(lambda: search(title))
            for result in results:
                anime_list.append(
                    BaseAnimeInfo(**result)
                )
        except Exception as e:
            logger.error(f"Error during searching for an anime: {e}")

        return anime_list

    @classmethod
    def get_anime_info(cls, anime_id: str) -> FullAnimeInfo:
        try:
            info = wrap_request(lambda: get_anime_info(anime_id))
            info = FullAnimeInfo(**info)
        except Exception as e:
            logger.error(f"Error during getting anime info: {e}")

        return info

    @classmethod
    def get_anime_links(cls, anime_id: str, episode: str) -> List[DownloadLinkInfo]:
        try:
            links = wrap_request(lambda: get_anime_links(anime_id, episode))
            # DownloadLinkInfo = [DownloadLinkInfo(**link) for link in links]
        except Exception as e:
            logger.error(f"Error during getting anime links: {e}")

        return links

AnimeFLVServiceDependency = Annotated[AnimeFLVService, Depends()]
