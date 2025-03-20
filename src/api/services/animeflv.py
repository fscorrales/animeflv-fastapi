__all__ = ["AnimeFLVService", "AnimeFLVServiceDependency"]

from typing import Annotated, List

from fastapi import Depends

from ..config import logger
from ..handlers import get_latest_animes
from ..models import LatestAnimes
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


AnimeFLVServiceDependency = Annotated[AnimeFLVService, Depends()]
