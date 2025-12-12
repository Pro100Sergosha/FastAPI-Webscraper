FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    chromium \
    git \
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

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]