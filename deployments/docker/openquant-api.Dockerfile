FROM python:3.11-slim

WORKDIR /app

# Phase 1 keeps the image minimal so local bootstrap stays simple.
COPY . /app

RUN pip install --no-cache-dir -e .

CMD ["uvicorn", "apps.api.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
