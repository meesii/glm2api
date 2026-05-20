FROM python:3.14-alpine3.21

WORKDIR /app

RUN apk add --no-cache curl ca-certificates \
    && addgroup -S glm2api \
    && adduser -S -G glm2api -h /app -s /sbin/nologin glm2api

COPY pyproject.toml ./

RUN apk add --no-cache --virtual .build-deps build-base libffi-dev openssl-dev \
    && pip install --no-cache-dir "curl-cffi>=0.7.0" \
    && apk del .build-deps

COPY src ./src

RUN find /app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
    find /app -name '*.py[cod]' -delete 2>/dev/null; \
    chown -R glm2api:glm2api /app

ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000

EXPOSE 8000

USER glm2api

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

CMD ["python", "-m", "glm2api"]
