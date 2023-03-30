import datetime
import logging
import os
from typing import Tuple, Dict, Union

import gspread
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError, TransportError, MalformedError
from gspread.exceptions import APIError, WorksheetNotFound
from pyasn1.error import PyAsn1Error


class EnquirySubmitter:
    """
    This class submits enquiries to a Google Sheet.
    """
    INTERNAL_ERROR_CATEGORY_CODENAME = "INTERNAL"
    CLIENT_ERROR_CATEGORY_CODENAME = "CLIENT"

    LOG_SEVERITY_INFO_CODENAME = "INFO"
    LOG_SEVERITY_CRITICAL_CODENAME = "CRITICAL"

    COLUMN_SPEC = {
        "Timestamp": "timestamp",
        "First Name": "first_name",
        "Last Name": "last_name",
        "Email": "email",
        "Company": "company",
        "Message": "message"
    }

    def __init__(
            self,
            gs_private_key: str,
            gs_client_email: str,
            gs_token_uri: str,
            spreadsheet_key: str,
            worksheet_title: str,
            timestamp_format: str,
    ):
        self.gs_private_key = gs_private_key
        self.gs_client_email = gs_client_email
        self.gs_token_uri = gs_token_uri
        self.spreadsheet_key = spreadsheet_key
        self.worksheet_title = worksheet_title
        self.timestamp_format = timestamp_format

        self.message = None
        self.detailed_message = None
        self.detailed_error = None
        self.error_category = None
        self.log_severity = None
        self.status_code = None

    def submit(self, body: Dict) -> bool:
        """
        It takes a dictionary of enquiry data, and appends it to a Google Sheet
        
        :param body: The body of the request
        :type body: Dict
        :return: A boolean value.
        """
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

        except MalformedError as exc:
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
