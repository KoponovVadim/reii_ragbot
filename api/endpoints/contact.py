from fastapi import APIRouter, Depends
from database import Database
from schemas.contact import ContactRequest, ContactResponse
from services.contact import process_contact_request
from database.connections import get_database


router = APIRouter()

@router.post("/contact", response_model=ContactResponse)
async def contact_form(
    request: ContactRequest,
    db: Database = Depends(get_database)
):
    result = await process_contact_request(db=db, request=request)
    return ContactResponse(
        **result)

