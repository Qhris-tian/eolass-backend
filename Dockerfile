FROM python:3.11-slim as python

ENV PYTHONUNBUFFERED=true

WORKDIR /app

RUN apt-get update -y && \
    apt-get install gcc -y && \
    apt-get install libpq-dev -y && \
    pip3 install poetry

COPY pyproject.toml .
COPY poetry.lock* .

RUN poetry config virtualenvs.create false && \
    poetry install && \
    apt-get remove gcc -y && \
    apt autoremove -y

COPY . /app

CMD ["uvicorn", "src.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "80"]