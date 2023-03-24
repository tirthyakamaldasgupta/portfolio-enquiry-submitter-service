import datetime
import os
from pathlib import Path
from typing import Tuple, Dict, Union

import gspread
from dotenv import load_dotenv


class EnquirySubmitter:
    INTERNAL_ERROR_CODENAME = "INTERNAL"
    EXTERNAL_ERROR_CODENAME = "EXTERNAL"
    
    ENV_KEYS = {
        "SPREADSHEET_KEY": "SPREADSHEET_KEY",
        "WORKSHEET_TITLE": "WORKSHEET_TITLE",
        "TIMESTAMP_FORMAT": "TIMESTAMP_FORMAT"
    }

    def __init__(self):
        self.spreadsheet_key = None
        self.worksheet_title = None
        self.timestamp_format = None
        
        self.message = None
        self.error = None
        self.error_type = None
        self.status_code = None

    def _load_env_vars(self) -> Tuple[bool, Union[str, None]]:
        load_dotenv()

        for key in EnquirySubmitter.ENV_KEYS.keys():
            if key not in os.environ:
                return False, key

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
        result, key = self._load_env_vars()

        if key and not result:
            self.error = f"Could not find key {key} in environment variables",
            self.error_type = EnquirySubmitter.INTERNAL_ERROR_CODENAME
            self.status_code = 404
            
            return False

        try:
            service_account = gspread.service_account(
                filename=os.path.join(
                    Path(__file__).parent.parent,
                    ".service-account.json"
                )
            )
        except FileNotFoundError:
            self.error = f"Could not find service account",
            self.error_type = EnquirySubmitter.INTERNAL_ERROR_CODENAME
            self.status_code = 404
            
            return False

        try:
            spreadsheet = service_account.open_by_key(self.spreadsheet_key)
        except gspread.exceptions.APIError as exc:
            self.error = exc.args[0]["message"],
            self.error_type = EnquirySubmitter.INTERNAL_ERROR_CODENAME
            self.status_code = int(exc.args[0]["code"])
            
            return False

        try:
            worksheet = spreadsheet.worksheet(self.worksheet_title)
        except gspread.exceptions.WorksheetNotFound:
            self.error = "Could not find worksheet",
            self.error_type = EnquirySubmitter.INTERNAL_ERROR_CODENAME
            self.status_code = 404

            return False

        worksheet.append_row([
            datetime.datetime.now().strftime(self.timestamp_format),
            body["first_name"],
            body["last_name"],
            body["email"],
            body["company"],
            body["message"]
        ])
        
        self.message = "Enquiry added successfully"
        self.status_code = 200

        return True


# a = EnquirySubmitter()
# 
# status, errors = a.submit({
#     "first_name": "Clyde",
#     "last_name": "Cronshaw",
#     "email": "ccronshaw3@theguardian.com",
#     "company": "Topicblab",
#     "message": "Nulla tellus. In sagittis dui vel nisl. Duis ac nibh."
# })
# 
# print(status)
# print(errors)
