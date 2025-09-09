## 主な改良点

- **Gemini API のエラーハンドリング追加**  
  レスポンスが `None` やエラーを返す場合の処理を実装

- **Logger モジュールの修正**  
  `error` メソッド追加と `info` メソッド利用への統一

- **型ヒントの修正**  
  `typing.List` のインポート漏れを修正

- **環境変数による Webhook 管理**  
  Discord Webhook URL をコードから取り除き、環境変数で設定

- **EventBridge スケジュール変更**  
  Cron式を日本時間23:35実行に変更

***Acknowledgments:***  
*This project is based on* [lambda-discord-rss-bot](https://github.com/mk668a/lambda-discord-rss-bot) *by mk668a.*

## セットアップ手順
### Discord Webhook URLの設定

1. Discord サーバーで Webhook を作成
2. `app/.env` ファイルに以下を追加：

# 概要

Discord RSS Bot

## Setting

```bash
aws configure
```

## Installation

Install the Serverless Framework globally

```bash
npm install -g serverless
```

## Create virtual environment

```bash
python -m venv ./venv
source ./venv/bin/activate
```

## Install required libraries

```bash
pip install -r requirements.txt
```

## Write required libraries

```bash
pip freeze > requirements.txt
```

## Run

```bash
python -m app.main
```

## Deploy

build

```bash
docker build -t discord-rss-bot-test .
```

build(Apple Silicon)

```bash
docker build --platform linux/amd64 -t discord-rss-bot-test .
```

deploy:prod

```bash
sls deploy
```
