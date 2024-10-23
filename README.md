# QuizApp

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Poetry**: Download and install
  Poetry [here](https://python-poetry.org/docs/)

- **Docker**: Download and install
   Docker [here](https://docs.docker.com/engine/install/)

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/PlzTrustMe/QuizApp
cd QuizApp
```

## Environment Setup
Copy .env.sample to .env and fill in the required data, if necessary

Installing project in development mode

```shell
poetry install --with test
```

Activate shell

```shell
poetry shell
```

## Running the Project

### To build and run the project

#### With Docker compose:
```bash
docker compose up --build
```

#### Local:
```bash
uvicorn app.main:create_app --reload --factory
```

## Running tests

#### Local:
```shell
pytest tests
```

#### With Dockerfile
Build:
```bash
docker build -t YOUR_TEST_CONTAINER_NAME -f test.Dockerfile .
```
Run:
```bash
docker run YOUR_TEST_CONTAINER_NAME
```

## Running linters

### Lint
```shell
ruff check
```

### Format
```shell
ruff format
```