FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
COPY ./ /app
WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000