from dataclasses import dataclass

from environs import Env


@dataclass
class BaseDBConfig:
    user: str
    password: str
    host: str
    port: int
    db_name: str

    def get_connection_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}"
            f":{self.port}/{self.db_name}"
        )


@dataclass
class DBConfig(BaseDBConfig):
    pass


@dataclass
class AlembicDBConfig(BaseDBConfig):
    pass


def load_alembic_config() -> AlembicDBConfig:
    env = Env()
    env.read_env(".env")

    config = AlembicDBConfig(
        user=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        host=env.str("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        db_name=env.str("POSTGRES_DB"),
    )

    return config
