from fastapi import APIRouter

from ..services import AnimeFLVServiceDependency
from ..models import BaseAnimeInfo, EpisodeInfo, FullAnimeInfo, DownloadLinkInfo
from typing import List

animeflv_router = APIRouter(prefix="/animeflv", tags=["AnimeFLV"])


@animeflv_router.get("/latest_animes", response_model=List[BaseAnimeInfo])
def latest_animes(animeflv: AnimeFLVServiceDependency):
    return animeflv.get_latest_animes()


@animeflv_router.get("/latest_episodes", response_model=List[EpisodeInfo])
def latest_episodes(animeflv: AnimeFLVServiceDependency):
    return animeflv.get_latest_episodes()


@animeflv_router.get("/search_anime", response_model=List[BaseAnimeInfo])    
def search_anime(title: str, animeflv: AnimeFLVServiceDependency):
    return animeflv.search_anime(title)


@animeflv_router.get("/get_anime_info", response_model=FullAnimeInfo)
def get_anime_info(anime_id: str, animeflv: AnimeFLVServiceDependency):
    return animeflv.get_anime_info(anime_id)


@animeflv_router.get("/get_anime_links", response_model=List[DownloadLinkInfo])
def get_anime_links(anime_id: str, episode: str, animeflv: AnimeFLVServiceDependency):
    return animeflv.get_anime_links(anime_id, episode)