import logging
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
        if enquiry_submitter.error_category == EnquirySubmitter.CLIENT_ERROR_CATEGORY_CODENAME:
            raise HTTPException(
                status_code=enquiry_submitter.status_code,
                detail=enquiry_submitter.detailed_error
            )

        elif enquiry_submitter.error_category == EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME:
            if enquiry_submitter.LOG_SEVERITY_CRITICAL_CODENAME == "CRITICAL":
                logging.critical(enquiry_submitter.detailed_error)

            raise HTTPException(
                status_code=enquiry_submitter.status_code,
                detail="Internal Server Error"
            )

    return {
        "message": enquiry_submitter.message
    }
