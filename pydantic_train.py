from pydantic import BaseModel, Field
from typing import List, Optional   

class QuestionRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Текст вопроса, не менее 3 символов.")

class AnswerResponse (BaseModel):
    answer :str 
    sources: List[str] = []
    confidence: Optional[float] = None


