# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y libimage-exiftool-perl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip && pip install uv
RUN uv pip install --system --editable .

COPY . .

RUN chmod +x start.sh
RUN SECRET_KEY=dummy python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["./start.sh"]
