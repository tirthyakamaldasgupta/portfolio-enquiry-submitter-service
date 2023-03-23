from fastapi import FastAPI
from .routes import portfolio_enquiry_submitter_router

app = FastAPI(
    title="Enquiry submitter service",
    description="""
    Enquiry submitter service
    """,
    version="0.0.1",
    contact={
        "name": "Tirthya Kamal Dasgupta",
        "email": "dasguptatirthyakamal@gmail.com"
    }
)

app.include_router(
    portfolio_enquiry_submitter_router,
    prefix="/enquiry"
)
