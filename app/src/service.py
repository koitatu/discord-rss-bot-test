import feedparser
from dataclasses import dataclass
from typing import List  # ← この行だけ追加
import requests
import json
from datetime import datetime, timedelta, timezone
from dateutil import parser
import time

from app.src import logger
from app.src.settings import GOOGLE_AI_STUDIO_API_KEY


@dataclass
class RssContent:
    title: str
    url: str
    published: str


def get_rss(endpoint: str) -> List[RssContent]:
    feed = feedparser.parse(endpoint)
    rss_list: List[RssContent] = []
    for entry in feed.entries:
        if not entry.get("link"):
            continue
        rss_content = RssContent(
            title=entry.title, url=entry.link, published=entry.published
        )
        rss_list.append(rss_content)
    return rss_list


def call_gemini(page_content: str, theme: str, bot_name: str):
    prompt = f"""あなたはRSSを発信する{bot_name}です。{bot_name}のような口調でRSS(テーマ:{theme})の内容を500文字以内で要約してください。改行は含めないでください。

{page_content}

"""
    uri = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_AI_STUDIO_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
    }
    response = requests.post(uri, headers=headers, data=json.dumps(data))

    json_data = response.json()

    # エラーハンドリングを追加
    if "error" in json_data:
        print(f"Gemini API エラー: {json_data['error']}")
        return "API設定エラーが発生しました。"
    
    candidates = json_data.get("candidates")
    if not candidates or len(candidates) == 0:
        print(f"Gemini APIからの無効なレスポンス: {json_data}")
        return "Gemini APIから有効なレスポンスを取得できませんでした。"

    response_text = (
        candidates[0].get("content").get("parts")[0].get("text")
    )

    return response_text


def call_main(urls: List[str], theme: str, bot_name: str, discord_url: str):
    # URLsからRSSのリストを取得
    rss_list = []
    for url in urls:
        rss_list.extend(get_rss(url))

    # publishedが24時間以内のものを取得
    rss_list = [
        rss
        for rss in rss_list
        if datetime.now(timezone.utc) - parser.parse(rss.published) < timedelta(days=1)
    ]

    # rss_listを最新順に並び替える
    rss_list = sorted(
        rss_list,
        key=lambda x: parser.parse(x.published),
        reverse=False,
    )

    # rss_listを10件ずつ分割する
    rss_lists = [rss_list[i : i + 10] for i in range(0, len(rss_list), 10)]

    for rss_list in rss_lists:
        # RSSの記事のタイトル一覧を作成（リンクを含む）
        parsed_content = "".join(
            [f"{i+1}. [{rss.title}]({rss.url})\n" for i, rss in enumerate(rss_list)]
        )
        # RSSの記事のタイトル一覧を作成
        content = "".join([f"{i}. {rss.title}\n" for i, rss in enumerate(rss_list)])

        for _ in range(3):  # 最大3回リトライ
            try:
                res = call_gemini(content, theme, bot_name)
                break
            except Exception as e:
                print(f"エラーが発生しました: {e}")  # logger.error の代わりに print を使用
                time.sleep(1)
        else:
            res = "エラーが発生しました。"

        requests.post(discord_url, json={"content": f"{res}\n{parsed_content}"})
