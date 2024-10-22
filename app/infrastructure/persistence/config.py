from dataclasses import dataclass


@dataclass
class DBConfig:
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
