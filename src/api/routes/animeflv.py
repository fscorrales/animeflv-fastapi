from typing import List

from fastapi import APIRouter

from ..models import LatestAnimes
from ..services import AnimeFLVServiceDependency

animeflv_router = APIRouter(prefix="/animeflv", tags=["AnimeFLV"])


@animeflv_router.get("/latest_animes")
def latest_animes(animeflv: AnimeFLVServiceDependency):
    return animeflv.get_latest_animes()
