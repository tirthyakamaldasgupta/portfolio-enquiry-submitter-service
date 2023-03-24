from fastapi import FastAPI
from .routes import portfolio_enquiry_submitter_router

app = FastAPI(
    title="Portfolio enquiry submitter service",
    description="""
    Portfolio enquiry submitter service
    """,
    version="0.0.0",
    contact={
        "name": "Tirthya Kamal Dasgupta",
        "email": "dasguptatirthyakamal@gmail.com"
    }
)

app.include_router(
    portfolio_enquiry_submitter_router,
    prefix="/enquiry"
)
