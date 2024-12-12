#!/bin/sh
# Flask gunicorn 사용 
# cd /app
# gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app

#FastAPI gunicorn 사용
cd /app
gunicorn main:app --workers 2 --bind 0.0.0.0:8080 --worker-class uvicorn.workers.UvicornWorker