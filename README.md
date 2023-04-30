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

## Lint project

```sh
poetry run ./scripts/lint.sh
```

## Run tests

This project uses pytests to run test.

```sh
poetry run ./scripts/test.sh
```

You can add any arguments to the command

e.g. adding `-x` to stop test on first failure

```sh
poetry run ./scripts/test.sh -x
```
