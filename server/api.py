import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .env_vars_loader import EnvVarsLoader, VarNotFoundException
from .routes import portfolio_enquiry_submitter_router

# Without configuring, the default level is WARNING.
# But logging is needed for every kind of operation like debugging, getting information etc.
# Configuring the log level and setting it to DEBUG

logging.basicConfig(level=logging.DEBUG)

# Creating an instance of the FastAPI app

app = FastAPI(
    title="Portfolio enquiry submitter service",
    description="""
    Portfolio enquiry submitter service
    """,
    version="0.0.6",
    contact={
        "name": "Tirthya Kamal Dasgupta",
        "email": "dasguptatirthyakamal@gmail.com"
    }
)

try:
    # Loading the environment variable "ENVIRONMENT"
    # If the variable is missing or its value doesn't match,
    # the server will not start

    env_vars = EnvVarsLoader(
        [
            "ENVIRONMENT"
        ]
    ).get_env_vars()

    environment = env_vars["ENVIRONMENT"]

    whitelisted_domains = []

    if environment == "DEV":
        whitelisted_domains = ["*"]

    elif environment == "STAGING":
        whitelisted_domains = ["*"]

    elif environment == "PROD":
        whitelisted_domains = ["*"]

    else:
        logging.critical("Invalid value for env var 'ENVIRONMENT'")

        sys.exit()
except VarNotFoundException as exc:
    logging.critical(exc)

    sys.exit()

# Allowing specific origins and methods for sending cross-origin requests

app.add_middleware(
    CORSMiddleware,
    allow_origins=whitelisted_domains,
    allow_methods=["OPTIONS", "POST"]
)

# Allowing specific domains to access this service,
# as mostly this will be an internal service which the portfolio client can access.
# It will not be accessible publicly.

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=whitelisted_domains
)

# Attaching the routes specified in "routes.py"

app.include_router(
    portfolio_enquiry_submitter_router,
    prefix="/enquiry"
)
