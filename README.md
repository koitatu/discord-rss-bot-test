# 概要

Discord RSS Bot origin by [lambda-discord-rss-bot](https://github.com/mk668a/lambda-discord-rss-bot)

***Acknowledgments:***  
*This project is based on* [lambda-discord-rss-bot](https://github.com/mk668a/lambda-discord-rss-bot) *by mk668a.*

## 主な改良点

- **Gemini API のエラーハンドリング追加**  
  レスポンスが `None` やエラーを返す場合の処理を実装

- **Logger モジュールの修正**  
  `error` メソッド追加と `info` メソッド利用への統一

- **型ヒントの修正**  
  `typing.List` のインポート漏れを修正

- **EventBridge スケジュール変更**  
  Cron式を日本時間23:35実行に変更

### フォルダ名を変更した場合の対応

プロジェクトディレクトリ名を変更すると、`node_modules` 内のパスがずれてプラグインやライブラリが読み込めなくなることがあります。  
その場合は以下の手順で依存関係を再インストールしてください。

- 古い依存関係を削除  
`rm -rf node_modules package-lock.json`

- 依存関係を再インストール  
`npm install`


## セットアップ手順
### 1. Discord Webhook URL の設定
1. Discord サーバーで Webhook を作成。
2. `app/main.py`の18行目: `discord_url = "DISCORD_WEBHOOK_URL_HERE"`を自身のDiscordWEBHOOKURLへ書き換える。

### 2. 環境変数ファイルの準備
1. `app/.env.sample`をコピーして、`app/.env` ファイルの`GOOGLE_AI_STUDIO_API_KEY`を自身のAPI_KEYへ書き換える。
2. `serverless-dotenv-plugin` をインストール  
```
npm install --save-dev serverless-dotenv-plugin
```

### 3. Python 環境の構築（ローカルテスト用・任意）

```
python -m venv ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Docker イメージのビルド
```
cd lambda-discord-rss-bot
docker build --platform linux/amd64 -t discord-rss-bot-test . # AppleSiliconの場合は必須。IntelArchでも動く。
```

### 5. ECR へのプッシュ

1. AWS アカウント ID を確認  
```
aws sts get-caller-identity --query Account --output text
```  
2. ECR リポジトリを作成（必要な場合）  
```
aws ecr create-repository --repository-name discord-rss-bot-test --region ap-northeast-1
```

3. Docker で ECR にログイン  

```
aws ecr get-login-password --region ap-northeast-1| docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.ap-northeast-1.amazonaws.com
```

4. イメージにタグ付け  
```
docker tag discord-rss-bot-test:latest <YOUR_ACCOUNT_ID>.dkr.ecr.ap-northeast-1.amazonaws.com/discord-rss-bot-test:latest
```

5. プッシュ  

```
docker push <YOUR_ACCOUNT_ID>.dkr.ecr.ap-northeast-1.amazonaws.com/discord-rss-bot-test:latest
```

#### AWS アカウントID を自動取得する方法 (おまけ)

##### Linux / macOS (bash/zsh)

```
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

##### Windows PowerShell
```
$env:ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
```

##### Windows CMD
```
REM AWS CLI でアカウントIDを取得して環境変数に設定
for /f "delims=" %%A in ('aws sts get-caller-identity --query Account --output text') do set ACCOUNT_ID=%%A
```

### 6. Serverless Framework でデプロイ

1. 環境変数をエクスポート  
```
export GOOGLE_AI_STUDIO_API_KEY="your_google_api_key_here"
```

2. デプロイ実行  
```
sls deploy --stage dev
```

### 7. 動作確認

- **手動テスト**  

```
sls invoke -f app --stage dev --data '{"bot_name":"developer"}'
```

- **ログ確認** 
```
aws logs tail /aws/lambda/discord-rss-bot-test-dev-app --since 5m --follow
```

- **スケジュール設定**  
EventBridge ルールが日本時間23:35に実行されることを確認  

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
