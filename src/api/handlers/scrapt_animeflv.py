#!/usr/bin/env python3
"""
Author : Fernando Corrales <fscpython@gmail.com>
Date   : 19-mar-2025
Purpose: Scrapt AnimeFlv
Source : https://medium.com/@jackcloudman/extrayendo-datos-de-animeflv-con-python-y-scrapy-1e76f6b3ff0f
Obs    : NOT TESTED / IMPLEMENTED YET
"""

__all__ = ["AnimeSpider"]

import argparse
import json
import re

import cloudscraper
import js2xml
import scrapy
from elasticsearch import Elasticsearch
from js2xml.utils.vars import get_vars
from scrapy.crawler import CrawlerProcess

from ..config import BASE_URL


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""Scrapes AnimeFLV for anime data.

            This script uses Scrapy to extract anime data from AnimeFLV.

            Example usage:
                python -m src.api.handlers.scrapt_animeflv
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    return parser.parse_args()


# --------------------------------------------------
class AnimeSpider(scrapy.Spider):
    """
    A Scrapy spider for scraping anime data from AnimeFLV.

    This spider extracts anime data from AnimeFLV, including titles, descriptions, genres, and episode information.

    Attributes:
        name (str): The name of the spider.
        base_url (str): The base URL of AnimeFLV.
        es (Elasticsearch): An Elasticsearch client for storing scraped data.
    """

    name = "AnimeSpider"
    base_url = BASE_URL
    es = Elasticsearch(hosts="localhost")

    def start_requests(self):
        """
        Starts the scraping process by sending a request to the AnimeFLV homepage.

        Yields:
            scrapy.Request: A request to the AnimeFLV homepage.
        """
        url = self.base_url + "browse?order=added"
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            cookies=response.cookies,
            headers=response.headers,
        )

    def parse(self, response):
        """
        Parses the HTML response from the AnimeFLV homepage.

        Extracts anime data from the page, including titles, descriptions, genres, and episode information.

        Args:
            response (scrapy.Response): The HTML response from the AnimeFLV homepage.

        Yields:
            dict: A dictionary containing the extracted anime data.
        """
        for a in response.xpath('.//article[@class="Anime alt B"]'):
            name = a.xpath(".//a/@href").extract_first()
            yield response.follow(
                self.base_url + name,
                callback=self.AnimeData,
                cookies=self.token,
                headers={"User-Agent": self.agent},
            )
        next_page = response.xpath('//a[@rel="next"]/@href').extract()
        if next_page:
            yield response.follow(
                self.base_url + next_page[0],
                callback=self.parse,
                cookies=self.token,
                headers={"User-Agent": self.agent},
            )

    def AnimeData(self, res):
        """
        Processes the extracted anime data and stores it in Elasticsearch.

        Args:
            res (dict): A dictionary containing the extracted anime data.

        Returns:
            None
        """
        data = {}
        data["id"] = int(re.findall("\/[0-9]+\/", res.request.url)[0][1:-1])
        data["rating"] = float(
            res.xpath('//span[@id="votes_prmd"]/text()').extract_first()
        )
        data["description"] = res.xpath(
            '//div[@class="Description"]/p/text()'
        ).extract_first()
        data["img"] = res.xpath("//figure//img/@src").extract_first()
        data["genre"] = [
            g.xpath("text()").extract_first()
            for g in res.xpath('//nav[@class="Nvgnrs"]//a')
        ]
        data["type"] = res.xpath(
            '//span[contains(@class,"Type")]/text()'
        ).extract_first()
        data["web_state"] = res.xpath(
            '//p[contains(@class,"AnmStts")]//span/text()'
        ).extract_first()
        data["votes"] = int(
            res.xpath('//span[@id="votes_nmbr"]/text()').extract_first()
        )
        script = res.xpath(
            '//script[contains(., "var anime_info")]/text()'
        ).extract_first()  # Obtenemos el script como string
        script_vars = get_vars(js2xml.parse(script))  # Parseamos y evaluamos
        anime_info = script_vars["anime_info"]
        data["name"] = anime_info[1]
        episodes_info = sorted(script_vars["episodes"])
        data["episodes_num"] = len(episodes_info)
        episodes = {}
        for e in episodes_info:
            episodes[e[0]] = {
                "link": "https://animeflv.net/ver/%s/%s-%s"
                % (e[1], anime_info[2], e[0]),
                "img": "https://cdn.animeflv.net/screenshots/%s/%s/th_3.jpg"
                % (anime_info[0], e[0]),
            }
        animeRel = []
        for a in res.xpath('//ul[contains(@class,"ListAnmRel")]//li'):
            aid = re.findall("\/[0-9]+\/", a.xpath("a/@href").extract_first())[0][1:-1]
            atype = a.xpath("text()").extract_first()
            name = a.xpath("a/text()").extract_first()
            animeRel.append({"id": aid, "name": name, "type": atype})
        data["animeRel"] = animeRel
        data["episodes"] = episodes
        try:
            res = self.es.index(
                index="animeflv2", doc_type="anime", body=data, id=data["id"]
            )
        except Exception as e:
            with open("animes/%s.json" % data["id"], "w") as f:
                json.dump(data, f)
                f.write(str(e))


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    try:
        proc = CrawlerProcess()
        proc.crawl(AnimeSpider)
        proc.start()
    except Exception as e:
        print(e)


# --------------------------------------------------
if __name__ == "__main__":
    main()

    # python -m src.api.handlers.scrapt_animeflv
