FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install  --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --gecos '' appuser

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn_worker.UvicornWorker", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]