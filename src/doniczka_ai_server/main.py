import os
from fastapi import FastAPI
from sqlalchemy import text
from doniczka_ai_server.database.postgres_client import PostgresClient

app = FastAPI()

@app.get("/")
async def root():
    postgres_client = PostgresClient.get_instance(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        db=os.getenv("POSTGRES_DB"),
        port=5432
    )

    with postgres_client.connect() as connection:
        result = connection.execute(text("SELECT 'hello world!'"))
        return {"message": result.scalar()}