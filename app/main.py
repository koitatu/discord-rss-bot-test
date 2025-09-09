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
        discord_url = "https://discord.com/api/webhooks/1414965406967529472/ZSefU4n3AxdqS5obJhwmiIvpaQfMNvsZ1iWZX3RuVCB4n-oCMStgwtfz6SaM07bsyyu8"
        call_main(urls, theme, bot_name, discord_url)
    else:
        logger.info("other")

    return {"message": event}


if __name__ == "__main__":
    # test
    handler({"bot_name": "developer"}, None)
