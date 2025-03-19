__all__ = ["wrap_request"]

import time
from typing import Callable

from cloudscraper.exceptions import CloudflareChallengeError


def wrap_request(func: Callable, count: int = 5):
    """
    Ejecuta una función que hace una solicitud HTTP y reintenta hasta `count` veces si falla.

    - Si la función devuelve `None` o una lista vacía `[]`, se considera fallo y reintenta.
    - Si ocurre un error, espera 5 segundos antes de reintentar.
    - Si después de `count` intentos sigue fallando, lanza una excepción.

    :param func: Función a ejecutar (debe pasarse sin ejecutar, por ejemplo `lambda: search("Dragon Ball Z")`).
    :param count: Número máximo de intentos antes de fallar.
    :return: Resultado de la función si es válido.
    """
    errors = []

    for attempt in range(count):
        try:
            res = func()  # Se ejecuta la función

            # Si la respuesta es vacía, lo consideramos un fallo y reintentamos
            if isinstance(res, list) and not res:
                raise ValueError("Respuesta vacía, reintentando...")

            return res  # Si la respuesta es válida, la retornamos

        except CloudflareChallengeError as e:
            errors.append(e)
            print(
                f"Intento {attempt + 1}/{count} fallido por Cloudflare, reintentando en 5 segundos..."
            )
        except Exception as e:
            errors.append(e)
            print(
                f"Intento {attempt + 1}/{count} fallido: {e}, reintentando en 5 segundos..."
            )

        time.sleep(5)  # Espera antes de reintentar

    raise Exception(f"Fallaron {count} intentos consecutivos. Errores: {errors}")
