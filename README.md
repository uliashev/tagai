# Tagai

## Getting Started

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (for containerized execution)
- uv (recommended for package management)

### Running Locally (Docker)

To run the full stack including the web app, database, Redis, and Celery worker:

```bash
docker compose up --build
```

The application will be available at http://localhost:8000.

### Running Locally (Manual)

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Start Redis**:
   Ensure you have a Redis server running on port 6379.

3. **Run Migrations**:
   ```bash
   uv run python manage.py migrate
   ```

4. **Start the Web Server**:
   ```bash
   uv run python manage.py runserver
   ```

5. **Start the Celery Worker**:
   Open a new terminal and run:
   ```bash
   uv run celery -A config worker -l info
   ```
