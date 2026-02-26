from databases import Database
from typing import List, Dict, Any
from uuid import UUID

async def create_conversation(db: Database, email:str) -> UUID:
    query = """
    INSERT INTO conversations (email) 
    VALUES (:email) 
    RETURNING id
    """

    result = await db.fetch_one(query=query, values={"email": email})
    return result["id"]

async def create_message( 
        db:Database, 
        conversation_id: UUID,
        role:str,
        content:str
        ) -> int:
    query = """
    INSERT INTO messages (conversation_id, role, content)
    VALUES (:conversation_id, :role, :content)
    RETURNING id
    """

    result = await db.fetch_one(
        query=query,
        values={
            "conversation_id": conversation_id,
            "role": role,
            "content": content
        }
    )
    return result["id"]

async def create_many_messages(
        db:Database,
        conversation_id: UUID,
        messages: List[Dict[str, Any]]
        ) -> None:
    query = """
    INSERT INTO messages (conversation_id, role, content)
    VALUES (:conversation_id, :role, :content)
    """

    values = [
        {
            "conversation_id": conversation_id,
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in messages
    ]

    await db.execute_many(query=query, values=values)   
    