from pydantic_train import QuestionRequest, AnswerResponse
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncpg
from database import database, questions
import datetime
from pydantic import BaseModel



class QuestionIn(BaseModel):
    text:str

class QuestionOut(BaseModel):
    id:int
    text:str
    created_at:str


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Connected to the database.")


    yield


    await database.disconnect()
    print("Disconnected from the database.")

app = FastAPI(lifespan=lifespan)


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:

    answer_text= f"Вы спросили: '{request.text}'. Но я пока ничего не знаю!"
    sources_list= ["Источник 1", "Источник 2"]
    return AnswerResponse(answer=answer_text, sources=sources_list, confidence=0.95)



@app.post("/questions",response_model=QuestionOut)
async def create_question(question: QuestionIn):
    query = questions.insert().values(
        question_text=question.text,
        created_at=str(datetime.datetime.now())
    )
    try:
        record_id = await database.execute(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    return{
        "id":record_id,
        "text":question.text,
        "created_at":str(datetime.datetime.now())   
    }

@app.get("/questions",response_model=list[QuestionOut])
async def read_questions(question_id:int):
    query = questions.select().where(questions.c.id == question_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return{
        "id":result["id"],
        "text":result["question_text"],
        "created_at":result["created_at"]
    }