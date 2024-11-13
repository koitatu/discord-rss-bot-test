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
