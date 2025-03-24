#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 24-mar-2025
Purpose: Get the real video url with yt-dlp
         Sirve para descargar videos o extraer enlaces directos de plataformas
         como: ✅ YouTube, Twitter, TikTok, Facebook, Instagram, Twitch, Reddit, etc.
         ✅ Algunos sitios de streaming como Vimeo y Dailymotion.
         ❌ No funciona con MEGA, Zippyshare o 1Fichier, porque no ofrecen streaming directo.
"""

__all__ = ["get_real_video_url"]

import argparse
import subprocess


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""This script retrieves the real video URL from a given platform (e.g., YouTube, Twitter, TikTok, etc.) 
        using yt-dlp. It supports platforms like YouTube, Twitter, Instagram, and other streaming services. 
        This is useful for downloading or extracting direct video links from websites that provide streaming content.
        
        Example usage:
            python -m src.api.handlers.get_real_video_url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "url",
        metavar="str",
        help="The URL of the video page from which to extract the real video URL.",
        type=str,
    )

    return parser.parse_args()


# --------------------------------------------------
def get_real_video_url(url: str) -> str:
    # Ejecutar yt-dlp dentro del entorno virtual
    cmd = ["yt-dlp", "-g", url]  # "-g" obtiene solo la URL del video
    real_url = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

    return real_url


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    try:
        real_url = get_real_video_url(url=args.url)
        print("Enlace directo:", real_url)
    except Exception as e:
        print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.get_real_video_url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
