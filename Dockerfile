FROM python:3.11-buster as builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /backend

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without test --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/backend/.venv \
    PATH="/backend/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app ./app

EXPOSE $SERVER_PORT

ENTRYPOINT ["sh", "-c", "uvicorn app.main:create_app --host $SERVER_HOST --port $SERVER_PORT --factory --reload"]