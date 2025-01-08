from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base


class Database:
    def __init__(self, database_url: str = None):
        """
        Initialize the database engine and session.
        If no URL is provided, use the default production database URL.
        """
        self.database_url = database_url
        self.engine = None
        self.session_local = None

    def configure(self, database_url: str):
        """
        Configure the database with the provided URL.
        """
        self.database_url = database_url
        self.engine = create_engine(self.database_url, pool_pre_ping=True)
        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_tables(self):
        """
        Create all tables in the database using the Base metadata.
        """
        if self.engine is None:
            raise ValueError("Database engine is not configured.")
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        """
        Drop all tables in the database using the Base metadata.
        """
        if self.engine is None:
            raise ValueError("Database engine is not configured.")
        Base.metadata.drop_all(bind=self.engine)

    def get_session(self):
        """
        Provide a session to interact with the database.
        """
        if self.session_local is None:
            raise ValueError("Database session is not configured.")
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()


# Production database instance
database = Database()
