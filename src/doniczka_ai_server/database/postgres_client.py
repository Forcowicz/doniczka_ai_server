import os
from sqlalchemy import create_engine


class PostgresClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            db = os.getenv("POSTGRES_DB")
            port = 5432

            cls._instance = create_engine(
                f"postgresql+psycopg://{user}:{password}@postgres-doniczka:{port}/{db}",
                echo=True,
            )
        return cls._instance
