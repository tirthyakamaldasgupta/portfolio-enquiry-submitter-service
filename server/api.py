import logging
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
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

whitelisted_domains = []

environment = os.environ.get("ENVIRONMENT")

if not environment:
    logging.critical("Deployment environment not found")

    sys.exit()

if environment == "DEV":
    whitelisted_domains = ["*"]
elif environment == "STAGING":
    whitelisted_domains = ["*"]
elif environment == "PROD":
    whitelisted_domains = ["https://portfolio-alpha-eight-91.vercel.app/"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=whitelisted_domains,
    allow_methods=["OPTIONS", "POST"]
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=whitelisted_domains
)

app.include_router(
    portfolio_enquiry_submitter_router,
    prefix="/enquiry"
)
