from sqlmodel import Session, SQLModel, create_engine

from ..config.database import DatabaseConfig
from ..utils.singleton import singleton


@singleton
class Database:
    def __init__(self, config=DatabaseConfig()) -> None:
        database_url = f"postgresql+psycopg://{config.username}:{config.password}@{config.host}:{config.port}/{config.db}"
        self.engine = create_engine(database_url, echo=True)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def session(self):
        return Session(self.engine)
