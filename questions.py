from sqlalchemy import Table, Column, Integer, String, Text


questions = Table(
    "questions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("question_text", Text),
    Column("answer_text", Text),
    Column("created_at", String)
)

