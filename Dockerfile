FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["app.main.handler"]