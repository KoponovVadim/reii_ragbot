from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
from typing import List, Literal

class MessageIn(BaseModel):
    role: Literal['user', 'assistant']
    content: str = Field(..., min_length=1, max_length=5000)

class ContactRequest(BaseModel):
    email: EmailStr
    messages: List[MessageIn] = Field (..., min_length=1)


class ContactResponse(BaseModel):
    conversation_id: UUID
    reply: str = "Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время."