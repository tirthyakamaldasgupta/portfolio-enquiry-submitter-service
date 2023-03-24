from typing import Dict

from fastapi import APIRouter, Body, HTTPException

from server.enquiry_submitter import EnquirySubmitter
from server.model import EnquirySchema

portfolio_enquiry_submitter_router = APIRouter()
enquiry_submitter = EnquirySubmitter()


@portfolio_enquiry_submitter_router.post(
    path="/",
    summary="Submit enquiries for portfolio"
)
async def submit_portfolio_enquiry(enquiry: EnquirySchema = Body(...)) -> Dict:
    body = enquiry.dict()

    status = enquiry_submitter.submit(body)

    if not status:
        if not enquiry_submitter.error_type == EnquirySubmitter.INTERNAL_ERROR_CODENAME:
            raise HTTPException(
                status_code=enquiry_submitter.status_code,
                detail=enquiry_submitter.error
            )

        # For internal errors, log them here.

    return {
        "message": enquiry_submitter.message
    }
