"""
Pydantic model for client information.
"""
from pydantic import BaseModel, EmailStr, Field

class Client(BaseModel):
    client_id: str = Field(..., description="Unique client identifier")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., min_length=7, max_length=20)
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "client_id": "12345",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+34123456789",
                "email": "john.doe@example.com"
            }
        }
