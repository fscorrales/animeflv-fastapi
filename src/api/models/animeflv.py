__all__ = [
    "BaseAnimeInfo",
    "FullAnimeInfo",
    "AnimeInfo",
    "EpisodeInfo",
    "EpisodeFormat",
    "DownloadLinkInfo",
]

from enum import Flag, auto
from typing import List, Optional, Union

from pydantic import BaseModel


# --------------------------------------------------
class EpisodeInfo(BaseModel):
    id: Union[str, int]
    anime: str
    image_preview: Optional[str] = None


class BaseAnimeInfo(BaseModel):
    id: Union[str, int]
    title: str
    poster: Optional[str] = None
    banner: Optional[str] = None
    synopsis: Optional[str] = None
    rating: Optional[str] = None
    debut: Optional[str] = None
    type: Optional[str] = None


class FullAnimeInfo(BaseAnimeInfo):
    genres: List[str]
    episodes: List[EpisodeInfo] 


# --------------------------------------------------
class AnimeInfo(BaseModel):
    id: Union[str, int]
    title: str
    poster: Optional[str] = None
    banner: Optional[str] = None
    synopsis: Optional[str] = None
    rating: Optional[str] = None
    genres: Optional[List[str]] = None
    debut: Optional[str] = None
    type: Optional[str] = None
    episodes: Optional[List[EpisodeInfo]] = None


class EpisodeFormat(Flag):
    Subtitled = auto()
    Dubbed = auto()


class DownloadLinkInfo(BaseModel):
    server: str
    url: str
