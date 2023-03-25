from typing import Optional

from pydantic import BaseModel


class EnquirySchema(BaseModel):
    """
    `EnquirySchema` is a `BaseModel` with `first_name`, `last_name`, `email`, `company` and `message` fields
    """
    first_name: str
    last_name: str
    email: str
    company: Optional[str] = None
    message: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Clyde",
                "last_name": "Cronshaw",
                "email": "ccronshaw3@theguardian.com",
                "company": "Topicblab",
                "message": "Nulla tellus. In sagittis dui vel nisl. Duis ac nibh."
            }
        }
