from fastapi import APIRouter, Body
from server.model import EnquirySchema

portfolio_enquiry_submitter_router = APIRouter()


@portfolio_enquiry_submitter_router.post(
    path="/",
    summary="Submit enquiries for portfolio"
)
async def submit_portfolio_enquiry(enquiry: EnquirySchema = Body(...)) -> dict:
    body = enquiry.dict()

    return {
        "message": "Note added successfully"
    }
