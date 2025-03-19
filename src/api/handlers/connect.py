"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 18-mar-2025
Purpose: Provides a class for interacting with the AnimeFLV website.
Source : https://github.com/jorgeajimenezl/animeflv-api
"""

__all__ = ["AnimeFLV"]

from typing import Optional, Type
from types import TracebackType
import cloudscraper
import certifi

# --------------------------------------------------
class AnimeFLV(object):
    """
    A class for interacting with the AnimeFLV website.

    This class provides methods for fetching anime data, including titles, descriptions, genres, and episode information.

    Attributes:
        _scraper (cloudscraper.CloudScraper): A CloudScraper instance for making requests to the AnimeFLV website.
        _session (requests.Session): A requests Session instance for making requests to the AnimeFLV website.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes an AnimeFLV instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            session (requests.Session, optional): A requests Session instance to use for making requests. Defaults to None.
        """
        session = kwargs.get("session", None)
        self._scraper = cloudscraper.create_scraper(session)
        # Configurar la verificación SSL con certifi
        self._scraper.verify = certifi.where()

    def close(self) -> None:
        """
        Closes the AnimeFLV instance.

        This method closes the underlying requests Session instance and CloudScraper instance.
        """
        self._scraper.close()

    def __enter__(self) -> "AnimeFLV":
        """
        Enters the AnimeFLV instance as a context manager.

        Returns:
            AnimeFLV: The AnimeFLV instance.
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """
        Exits the AnimeFLV instance as a context manager.

        Args:
            exc_type (type): The type of exception that occurred.
            exc_val (Exception): The exception that occurred.
            exc_tb (traceback): The traceback of the exception.
        """
        self.close()