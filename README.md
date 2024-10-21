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

#### With Dockerfile:

```bash
docker build -t YOUR_CONTAINER_NAME .    
```
```bash
 docker run --env-file .env -p 8000:8000 YOUR_CONTAINER_NAME      
```

#### Local:

```bash
uvicorn app.main:create_app --reload --factory  
```

## Running tests

```shell
pytest tests
```