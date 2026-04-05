FROM python:3.12-slim

WORKDIR /app

RUN groupadd --system --gid 1001 appuser && \
    useradd --system --uid 1001 --gid appuser appuser

COPY pyproject.toml .
COPY app/ ./app/

RUN pip install --no-cache-dir .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
