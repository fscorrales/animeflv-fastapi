from fastapi import APIRouter

from typing import List

from ..services import AnimeFLVService
from ..models import LatestAnimes

animeflv_router = APIRouter(prefix="/animeflv", tags=["AnimeFLV"])


@animeflv_router.get("/latest_animes")
async def latest_animes(animeflv: AnimeFLVService, response_model: None):
    return animeflv.get_latest_animes()