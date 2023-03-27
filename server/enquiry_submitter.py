import datetime
import logging
import os
from typing import Tuple, Dict, Union

import gspread
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError, TransportError
from gspread.exceptions import APIError, WorksheetNotFound
from pyasn1.error import PyAsn1Error


class EnquirySubmitter:
    """
    This class submits enquiries to the database.
    """
    INTERNAL_ERROR_CATEGORY_CODENAME = "INTERNAL"
    CLIENT_ERROR_CATEGORY_CODENAME = "CLIENT"

    LOG_SEVERITY_INFO_CODENAME = "INFO"
    LOG_SEVERITY_CRITICAL_CODENAME = "CRITICAL"

    ENV_KEYS = {
        "GS_PRIVATE_KEY": "GS_PRIVATE_KEY",
        "GS_CLIENT_EMAIL": "GS_CLIENT_EMAIL",
        "GS_TOKEN_URI": "GS_TOKEN_URI",
        "SPREADSHEET_KEY": "SPREADSHEET_KEY",
        "WORKSHEET_TITLE": "WORKSHEET_TITLE",
        "TIMESTAMP_FORMAT": "TIMESTAMP_FORMAT"
    }

    COLUMN_SPEC = {
        "Timestamp": "timestamp",
        "First Name": "first_name",
        "Last Name": "last_name",
        "Email": "email",
        "Company": "company",
        "Message": "message"
    }

    def __init__(self):
        """
        The function is called when the class is instantiated. It sets the instance attributes to None.
        """
        self.gs_private_key = None
        self.gs_client_email = None
        self.gs_token_uri = None
        self.spreadsheet_key = None
        self.worksheet_title = None
        self.timestamp_format = None

        self.message = None
        self.detailed_message = None
        self.detailed_error = None
        self.error_category = None
        self.log_severity = None
        self.status_code = None

    def _load_env_vars(self) -> Tuple[bool, Union[str, None]]:
        """
        It loads the environment variables from the `.env` file and stores them in the class instance
        :return: A tuple of two values. The first is a boolean value indicating whether the environment
        variables were loaded successfully. The second is either a string indicating the name of the
        environment variable that was not found, or None if all environment variables were found.
        """
        load_dotenv()

        for key in EnquirySubmitter.ENV_KEYS.keys():
            if key not in os.environ:
                return False, key

        self.gs_private_key = os.environ.get(
            EnquirySubmitter.ENV_KEYS["GS_PRIVATE_KEY"]
        )

        self.gs_client_email = os.environ.get(
            EnquirySubmitter.ENV_KEYS["GS_CLIENT_EMAIL"]
        )

        self.gs_token_uri = os.environ.get(
            EnquirySubmitter.ENV_KEYS["GS_TOKEN_URI"]
        )

        self.spreadsheet_key = os.environ.get(
            EnquirySubmitter.ENV_KEYS["SPREADSHEET_KEY"]
        )

        self.worksheet_title = os.environ.get(
            EnquirySubmitter.ENV_KEYS["WORKSHEET_TITLE"]
        )

        self.timestamp_format = os.environ.get(
            EnquirySubmitter.ENV_KEYS["TIMESTAMP_FORMAT"]
        )

        return True, None

    def submit(self, body: Dict) -> bool:
        """
        It takes a dictionary of enquiry data, and appends it to a Google Sheet
        
        :param body: The body of the request
        :type body: Dict
        :return: A boolean value.
        """
        result, key = self._load_env_vars()

        if key and not result:
            self.detailed_error = f"Key \"{key}\" absent or malformed in environment variables"
            self.error_category = EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME
            self.log_severity = EnquirySubmitter.LOG_SEVERITY_CRITICAL_CODENAME
            self.status_code = 500

            return False

        try:
            service_account = gspread.service_account_from_dict({
                "private_key": self.gs_private_key,
                "client_email": self.gs_client_email,
                "token_uri": self.gs_token_uri
            })

        except PyAsn1Error as exc:
            self.detailed_error = exc
            self.error_category = EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME
            self.log_severity = EnquirySubmitter.LOG_SEVERITY_CRITICAL_CODENAME
            self.status_code = 500

            return False

        try:
            spreadsheet = service_account.open_by_key(self.spreadsheet_key)

        except RefreshError as exc:
            self.detailed_error = exc
            self.error_category = EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME
            self.log_severity = EnquirySubmitter.LOG_SEVERITY_CRITICAL_CODENAME
            self.status_code = 500

            return False

        except TransportError as exc:
            self.detailed_error = exc
            self.error_category = EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME
            self.log_severity = EnquirySubmitter.LOG_SEVERITY_CRITICAL_CODENAME
            self.status_code = 500

            return False

        except APIError as exc:
            self.detailed_error = exc
            self.error_category = EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME
            self.log_severity = EnquirySubmitter.LOG_SEVERITY_CRITICAL_CODENAME
            self.status_code = int(exc.args[0]["code"])

            return False

        try:
            worksheet = spreadsheet.worksheet(self.worksheet_title)

        except WorksheetNotFound as exc:
            self.detailed_error = exc
            self.error_category = EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME
            self.log_severity = EnquirySubmitter.LOG_SEVERITY_CRITICAL_CODENAME
            self.status_code = 500

            return False

        column_names = worksheet.row_values(1)

        if not column_names == [key for key in EnquirySubmitter.COLUMN_SPEC.keys()]:
            self.detailed_error = "Column specs doesn't match with sheet columns"
            self.error_category = EnquirySubmitter.INTERNAL_ERROR_CATEGORY_CODENAME
            self.log_severity = EnquirySubmitter.LOG_SEVERITY_CRITICAL_CODENAME
            self.status_code = 500

            return False

        data = [datetime.datetime.fromtimestamp(body["timestamp"] / 1000).strftime(self.timestamp_format)]

        for index in range(1, len(column_names)):
            data.append(
                body[EnquirySubmitter.COLUMN_SPEC[column_names[index]]]
                if column_names[index] in EnquirySubmitter.COLUMN_SPEC.keys() and
                EnquirySubmitter.COLUMN_SPEC[column_names[index]] in body.keys() else None
            )

        response = worksheet.append_row(data)

        self.message = "Enquiry added successfully"
        self.detailed_message = response
        self.log_severity = EnquirySubmitter.LOG_SEVERITY_INFO_CODENAME
        self.status_code = 200

        return True
