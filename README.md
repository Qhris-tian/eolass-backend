# eolass-backend

## Set environment variables

```sh
cp .env.example .env
```

## Project Setup

### Install [Poetry](https://python-poetry.org/docs/#installation)

### Install application dependencies

```sh
poetry install
```

### Start application server

```sh
poetry run uvicorn main:app --reload
```

## Project Setup with Docker

### Build and start containers

```sh
docker compose up -d --build
```
