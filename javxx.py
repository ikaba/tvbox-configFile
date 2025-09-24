# -*- coding: utf-8 -*-
import requests
import re
import json
import traceback
import sys
from urllib.parse import quote
# -*- coding: utf-8 -*-
# TVBox 自定义爬虫脚本 - javxx 版

import requests
from bs4 import BeautifulSoup
import re

class Spider:
    def __init__(self):
        self.base_url = "https://www.javxxx.com"   # 替换成实际的 javxx 域名
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def searchContent(self, key, quick=False):
        """
        搜索影片
        :param key: 搜索关键词 (番号/演员名)
        :return: 列表，每个元素包含 {vod_id, vod_name, vod_pic, vod_remarks}
        """
        url = f"{self.base_url}/search/{key}"
        res = requests.get(url, headers=self.headers, timeout=10)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        videos = []
        for item in soup.select(".movie-box"):
            title = item.select_one(".title").get_text(strip=True)
            href = item.get("href")
            pic = item.select_one("img").get("src")
            remark = item.select_one(".meta").get_text(strip=True) if item.select_one(".meta") else ""

            videos.append({
                "vod_id": href,
                "vod_name": title,
                "vod_pic": pic,
                "vod_remarks": remark
            })
        return videos

    def detailContent(self, ids):
        """
        获取影片详情
        :param ids: searchContent 里返回的 vod_id
        """
        url = ids[0]
        res = requests.get(url, headers=self.headers, timeout=10)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.select_one("h3").get_text(strip=True)
        pic = soup.select_one(".bigImage img").get("src")
        desc = soup.select_one(".info").get_text(" ", strip=True)

        vod = {
            "vod_id": url,
            "vod_name": title,
            "vod_pic": pic,
            "vod_content": desc,
            "vod_play_from": "javxx",
            "vod_play_url": "在线观看$" + url
        }
        return [vod]

    def playerContent(self, flag, id, vipFlags):
        """
        播放器接口，这里只是示例，直接返回原页面链接
        """
        return {
            "parse": 0,
            "playUrl": "",
            "url": id,
            "header": self.headers
        }


# 测试运行
if __name__ == "__main__":
    spider = Spider()
    results = spider.searchContent("ABP-123")
    print("搜索结果：", results[:3])

    if results:
        detail = spider.detailContent([results[0]["vod_id"]])
        print("详情：", detail)
