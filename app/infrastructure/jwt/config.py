from dataclasses import dataclass


@dataclass
class JWTConfig:
    key: str
    algorithm: str


@dataclass
class Auth0Config:
    domain: str
    audience: str
