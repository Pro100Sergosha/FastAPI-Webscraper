# FastAPI WebScraper

**FastAPI WebScraper** is a high-performance asynchronous web scraping service built with Python 3.13. It utilizes `nodriver` to navigate websites (including SPAs with dynamic content), automatically cleans HTML, and converts it into Markdown, optimized for RAG systems and LLMs.

## 🚀 Key Features

* **Asynchronous Engine**: Maximum performance thanks to `asyncio` and `nodriver` (an alternative to Selenium/Puppeteer).
* **JavaScript Support**: Renders dynamic content and bypasses basic anti-bot systems.
* **HTML to Markdown**: Smart content conversion: removes ads, navigation, and scripts, preserving useful text and metadata.
* **Task Scheduler**: Built-in Cron scheduler (`APScheduler`) for regular data collection.
* **REST API**: Convenient interface for managing tasks and retrieving statuses.
* **Docker Ready**: Fully containerized for quick deployment.

## 🛠 Tech Stack

* **Python**: 3.13
* **Framework**: FastAPI
* **Scraper**: Nodriver
* **Parsing**: BeautifulSoup4 + Markdownify
* **Task Management**: Asyncio Queue + Local JSON Store
* **Package Manager**: uv

## 📋 Requirements

* Docker & Docker Compose (recommended)
* **OR** Python 3.13+ and an installed Chrome/Chromium browser (for local execution)

## ⚙️ Installation and Running

### Running via Docker (Recommended)

1.  Clone the repository:
    ```bash
    git clone https://github.com/Pro100Sergosha/FastAPI-Webscraper.git
    ```
    
    ```bash
    cd FastAPI-Webscraper
    ```

2.  Create the configuration file:
    ```bash
    cp .env.example .env
    ```

3.  Start the services:
    ```
    cd docker
    ```
    ```
    docker-compose up --build
    ```

The server will be available at: `http://localhost:8000`

### Local Run (without Docker)

1.  Install the `uv` package manager:
    ```
    pip install uv
    ```

2.  Install dependencies:
    ```
    uv sync
    ```

3.  Start the server:
    ```
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

## 🔧 Configuration (.env)

Application settings are located in the `.env` file. Key parameters:

| Parameter | Description | Default Value |

| `APP_NAME` | Application name | FastAPI WebScraper |

| `TARGET_URL` | URL for automatic scheduled scraping | https://www.example.com/ |

| `MAX_CRAWL_DEPTH` | Recursive link crawling depth | 3 |

| `MAX_WORKERS` | Number of concurrent threads/tabs | 5 |

| `REQUEST_TIMEOUT` | Page load timeout (sec) | 30 |

| `SCRAPE_SCHEDULE_TIME` | Daily run time (HH:MM) | 12:00 |

| `LOG_LEVEL` | Logging level | INFO |

## 🔌 API Interface

Swagger UI documentation is available at: `/docs`

### 1. Trigger Scraping (Trigger)

Starts a task to collect data for the specified URL.

**Request:**
`POST /api/v1/scraper/trigger`

```json
{
  "url": "[https://fastapi.tiangolo.com/]"
}
```

**Response:**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "queued"
}
```

### 2. Check Status (Status)

Retrieves information about the current progress of a task.

**Request:**
`GET /api/v1/scraper/status/{task_id}`

**Response:**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "running",
  "url": "[https://fastapi.tiangolo.com/]",
  "processed_links": 15,
  "total_links_found": 42,
  "created_at": "2023-10-27T10:00:00",
  "estimated_time_remaining": "0:02:30"
}
```

### 3. View Logs (Logs)

Returns the latest entries from the log file.

**Request:**
`GET /api/v1/scraper/logs?limit=50`

**Response:**
```json
{
  "logs": [
    "2023-10-27 10:00:01 - uvicorn.access - INFO - Application startup complete.",
    "2023-10-27 10:05:23 - app.services.crawler - INFO - === Starting crawling: task_id | Max Depth: 3 ==="
  ]
}
```

## 📂 Project Structure

```text
fastapi-webscraper/
├── app/
│   ├── api/            # API routes and dependencies
│   ├── core/           # Configuration, logging, scheduler
│   ├── models/         # Pydantic data models
│   ├── services/       # Core logic (Crawler, Parser, Storage)
│   └── main.py         # Application entry point
├── docker/             # Dockerfile and docker-compose.yml
├── logs/               # Application logs
├── storage/            # Saved data
│   ├── html/           # Raw HTML page code
│   └── markdown/       # Processed Markdown files
├── tests/              # Pytest tests
├── .env.example        # Environment variable template
├── pyproject.toml      # Project configuration and dependencies
└── uv.lock             # Dependency lock file
```

## 🧪 Testing

The project is covered by tests using `pytest`.

To run tests locally:
```bash
uv run pytest
```

To run tests inside the Docker container:
```bash
docker exec -it fastapi_webscraper pytest
```

## 🔮 Future Extensibility

This project is architected to support future integration with **RAG (Retrieval-Augmented Generation)** systems and advanced data pipelines:

* **Vector Database Integration**: Abstract storage interfaces designed to easily switch from the file system to vector databases (e.g., Pinecone, Qdrant, Milvus).
* **Advanced Document Processing**: Support for pluggable processors to handle complex chunking strategies (configurable size and overlap).
* **Embedding Hooks**: Extensible points for generating vector embeddings directly from the processed Markdown content.
* **Metadata Enrichment**: Schema designed to support additional metadata (timestamps, source tags, content classification) for better retrieval accuracy.

