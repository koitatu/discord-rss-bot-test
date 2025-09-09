FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# Lambda handler として指定
CMD ["app.main.handler"]
