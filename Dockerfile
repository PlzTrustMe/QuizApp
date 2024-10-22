FROM python:3.11-slim-buster

WORKDIR /app

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY . .

RUN poetry install --no-root --without test && rm -rf $POETRY_CACHE_DIR

#RUN poetry install

#EXPOSE 8000
#
#CMD ["sh", "-c", "poetry run uvicorn app.main:create_app --host $SERVER_HOST --port $SERVER_PORT --factory --reload"]