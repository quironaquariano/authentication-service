from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.session_local = sessionmaker(autocommit=False, bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        """Remove todas as tabelas definidas no modelo Base."""
        Base.metadata.drop_all(bind=self.engine)

    def get_session(self):
        db = self.session_local()
        print(f"Using database engine: {self.engine.url}")  # Depuração
        try:
            yield db
        finally:
            db.close()
