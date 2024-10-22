FROM python:3.11-buster as builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /backend

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --with test --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/backend/.venv \
    PATH="/backend/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app ./app
COPY tests ./tests

ENTRYPOINT ["sh", "-c", "pytest tests --maxfail=1 --disable-warnings"]
