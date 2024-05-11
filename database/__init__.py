from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.app_config import config


class Database:
    def __init__(self):
        self.base = declarative_base()
        self.engine = create_async_engine(config.db_string, echo=False)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    def get_session(self) -> AsyncSession:
        return self.session()


database = Database()
