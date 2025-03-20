__all__ = ["AnimeFLVService", "AnimeFLVServiceDependency"]

from typing import Annotated, List

from fastapi import Depends

from ..handlers import get_latest_animes
from ..models import LatestAnimes
from ..config import logger


class AnimeFLVService:
    @classmethod
    async def get_latest_animes(cls) -> List[LatestAnimes]:
        try:
            results = await wrap_request(lambda: get_latest_animes())
            anime_list = []
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