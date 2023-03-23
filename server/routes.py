from fastapi import APIRouter, Body
from server.model import EnquirySchema

portfolio_enquiry_submitter_router = APIRouter()


@portfolio_enquiry_submitter_router.post("/")
async def submit_portfolio_enquiry(enquiry: EnquirySchema = Body(...)) -> dict:
    body = enquiry.dict()

    return {
        "message": "Note added successfully"
    }
