__all__ = ["api_router"]

from fastapi import APIRouter


from .animeflv import animeflv_router

api_router = APIRouter(prefix="/api")
api_router.include_router(animeflv_router)