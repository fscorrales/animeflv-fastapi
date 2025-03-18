__all__ = ["AnimeFLV"]

from types import TracebackType
from typing import Optional, Type

import certifi
import cloudscraper


# --------------------------------------------------
class AnimeFLV(object):
    def __init__(self, *args, **kwargs):
        session = kwargs.get("session", None)
        self._scraper = cloudscraper.create_scraper(session)
        # Configurar la verificación SSL con certifi
        self._scraper.verify = certifi.where()

    def close(self) -> None:
        self._scraper.close()

    def __enter__(self) -> "AnimeFLV":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()
