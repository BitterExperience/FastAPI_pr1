FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --timeout=100 --retries=10 -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

RUN adduser --disabled-password --gecos '' appuser

COPY --chown=appuser:appuser . .

RUN mkdir -p /app/data && chown appuser:appuser /app/data

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && gunicorn app.main:app --workers 4 --worker-class uvicorn_worker.UvicornWorker --bind 0.0.0.0:8000 --access-logfile -"]