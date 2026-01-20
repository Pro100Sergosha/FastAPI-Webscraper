FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    chromium \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    NODRIVER_BROWSER_PATH=/usr/bin/chromium

COPY pyproject.toml uv.lock ./

RUN sed -i 's/>=3.14/>=3.13/' pyproject.toml

RUN uv sync

COPY . .


COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

EXPOSE 8000

CMD ["xvfb-run", "--auto-servernum", "uv", "run", "uvicorn", "app.runner.asgi:app", "--host", "0.0.0.0", "--port", "8000"]