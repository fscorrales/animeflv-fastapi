__all__ = ["AnimeFLVService", "AnimeFLVServiceDependency"]

from typing import Annotated, List

from fastapi import Depends

from ..config import logger
from ..handlers import get_latest_animes, get_latest_episodes
from ..models import EpisodeInfo, LatestAnimes
from ..utils import wrap_request


class AnimeFLVService:
    @classmethod
    def get_latest_animes(cls) -> List[LatestAnimes]:
        try:
            anime_list = []
            results = wrap_request(lambda: get_latest_animes())
            for result in results:
                anime_list.append(
                    LatestAnimes(
                        id=result.id,
                        title=result.title,
                        synopsis=result.synopsis,
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
            logger.error(f"Error during getting latest animes: {e}")

        return episodes_list


AnimeFLVServiceDependency = Annotated[AnimeFLVService, Depends()]
