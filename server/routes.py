import logging
import sys

from typing import Dict

from fastapi import APIRouter, Body, HTTPException, Request

from server.enquiry_submitter import EnquirySubmitter
from server.env_vars_loader import EnvVarsLoader, VarNotFoundException
from server.model import EnquirySchema

try:
    env_vars = EnvVarsLoader(
        [
            "GS_PRIVATE_KEY",
            "GS_CLIENT_EMAIL",
            "GS_TOKEN_URI",
            "SPREADSHEET_KEY",
            "WORKSHEET_TITLE",
            "TIMESTAMP_FORMAT"
        ]
    ).get_env_vars()
except VarNotFoundException as exc:
    logging.critical(exc)

    sys.exit()

portfolio_enquiry_submitter_router = APIRouter()

enquiry_submitter = EnquirySubmitter(
    gs_private_key=env_vars["GS_PRIVATE_KEY"].replace("\\n", "\n"),
    gs_client_email=env_vars["GS_CLIENT_EMAIL"],
    gs_token_uri=env_vars["GS_TOKEN_URI"],
    spreadsheet_key=env_vars["SPREADSHEET_KEY"],
    worksheet_title=env_vars["WORKSHEET_TITLE"],
    timestamp_format=env_vars["TIMESTAMP_FORMAT"],
)


@portfolio_enquiry_submitter_router.post(
    path="/",
    summary="Submit enquiries for portfolio"
)
async def submit_portfolio_enquiry(request: Request, enquiry: EnquirySchema = Body(...)) -> Dict:
    """
    "Submit enquiries for portfolio"
    
    The function is a POST request, and it takes in a JSON body
    
    :param request:
    :param enquiry: EnquirySchema = Body(...)
    :type enquiry: EnquirySchema
    :return: A dictionary with a message key and a value of the message returned from the enquiry
    submitter.
    """
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

    logging.info(enquiry_submitter.detailed_message)

    return {
        "message": enquiry_submitter.message
    }
