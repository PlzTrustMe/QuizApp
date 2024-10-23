from dataclasses import dataclass


@dataclass
class RedisConfig:
    password: str
    host: str
    port: int
    db: int

    def get_connection_url(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
