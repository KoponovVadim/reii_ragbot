from databases import Database
from uuid import UUID
from typing import List, Dict, Any
from schemas.contact import ContactRequest
from database.repositories import contact as contact_repo


async def process_contact_request(
        db:Database,
        request: ContactRequest,
        assistant_reply: str = "Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время."
        ) -> Dict[str, Any]:

    async with db.transaction():
        conversation_id = await contact_repo.create_conversation(
            db=db,
            email=request.email
        )

        all_messages = []

        for msg in request.messages:
            all_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        all_messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

        await contact_repo.create_many_messages(
            db=db,
            conversation_id=conversation_id,
            messages=all_messages
        )
        

        # Потом добавим фоновую отправку email

        return {
            "conversation_id": conversation_id,
            "reply": assistant_reply
        }