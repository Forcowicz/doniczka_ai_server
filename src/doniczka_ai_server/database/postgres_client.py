from sqlalchemy import create_engine

class PostgresClient:
    _instance = None

    @classmethod
    def get_instance(cls, user: str, password: str, db: str, port: int):
        if cls._instance is None:
            cls._instance = create_engine(f"postgresql+psycopg://{user}:{password}@postgres:{port}/{db}")
        return cls._instance