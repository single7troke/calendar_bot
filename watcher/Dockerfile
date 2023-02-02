FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
COPY ./ /watcher
WORKDIR /watcher

RUN pip install -r requirements.txt --no-cache-dir
