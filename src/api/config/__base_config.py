__all__ = ["BASE_URL", "BROWSE_URL", "ANIME_VIDEO_URL", "ANIME_URL", "BASE_EPISODE_IMG_URL", "logger"]

import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

# Fixing a "bycript issue"
logging.getLogger("passlib").setLevel(logging.ERROR)

BASE_URL = "https://animeflv.net"
BROWSE_URL = "https://animeflv.net/browse"
ANIME_VIDEO_URL = "https://animeflv.net/ver/"
ANIME_URL = "https://animeflv.net/anime/"
BASE_EPISODE_IMG_URL = "https://cdn.animeflv.net/screenshots/"