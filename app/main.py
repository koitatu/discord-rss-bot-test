from app.src.logger import logger
from app.src.service import call_main


def handler(event, context):
    logger.info(event)
    bot_name = event.get("bot_name")

    if bot_name == "developer":
        theme = "エンジニア"
        urls = [
            "https://www.publickey1.jp/atom.xml",
            "https://ai-data-base.com/feed",
            "https://zenn.dev/topics/flutter/feed",
        ]
        bot_name = "兄貴"
        discord_url = "https://discord.com/api/webhooks/1303390906929381507/XrrS863ltJbYFiTPvX6dYeD6OuedEezHqFCkjqRU6Xiu2c66kXbXUU5P46dBI8Swb0pQ"

        call_main(urls, theme, bot_name, discord_url)
    else:
        logger.info("other")

    return {"message": event}


if __name__ == "__main__":
    # test
    handler({"bot_name": "developer"}, None)
