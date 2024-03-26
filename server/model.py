from typing import Optional

from pydantic import BaseModel


class EnquirySchema(BaseModel):
    """
    `EnquirySchema` is a `BaseModel` with `firstName`, `middleName`, `lastName`, `email`, `company` and `message` fields
    """
    timeStamp: int
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    email: str
    company: Optional[str] = None
    message: str

    class Config:
        schema_extra = {
            "example": {
                "firstName": "Clyde",
                "middleName": "Doe",
                "lastName": "Cronshaw",
                "email": "ccronshaw3@theguardian.com",
                "company": "Topicblab",
                "message": "Nulla tellus. In sagittis dui vel nisl. Duis ac nibh."
            }
        }
