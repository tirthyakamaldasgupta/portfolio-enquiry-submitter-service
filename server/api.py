import logging
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import portfolio_enquiry_submitter_router
from dotenv import load_dotenv

app = FastAPI(
    title="Portfolio enquiry submitter service",
    description="""
    Portfolio enquiry submitter service
    """,
    version="0.0.4",
    contact={
        "name": "Tirthya Kamal Dasgupta",
        "email": "dasguptatirthyakamal@gmail.com"
    }
)

load_dotenv()

origins = []

environment = os.environ.get("ENVIRONMENT")

if not environment:
    logging.critical("Deployment environment not found")

    sys.exit()

if environment == "DEV":
    allow_origins = ["*"],
elif environment == "STAGING":
    allow_origins = ["*"]
elif environment == "PROD":
    allow_origins = ["https://portfolio-enquiry-submitter-service.vercel.app/"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
)

app.include_router(
    portfolio_enquiry_submitter_router,
    prefix="/enquiry"
)
