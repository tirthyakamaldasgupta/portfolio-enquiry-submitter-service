from fastapi import FastAPI
from .routes import portfolio_enquiry_submitter_router

app = FastAPI()

app.include_router(
    portfolio_enquiry_submitter_router,
    prefix="/enquiry"
)
