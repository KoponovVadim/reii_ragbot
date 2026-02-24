from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
import os

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://user:password@localhost/dbname")
database = Database(DATABASE_URL)
metadata = MetaData()

questions = Table(
    "questions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("question_text", String),
    Column("created_at", DateTime),
)

