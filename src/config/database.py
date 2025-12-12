from .base import Settings


class DatabaseConfig(Settings):
    host: str
    port: int
    username: str
    password: str
    db: str

    class Config:
        env_prefix = "database_"
