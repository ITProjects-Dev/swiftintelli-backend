from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

class FAQRequest(BaseModel):
    faq_id: int

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(
        ...,
        min_length=1,
        max_length=300
    )


class FeedbackRequest(BaseModel):
    log_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=0, le=1)

class EndChatRequest(BaseModel):
    session_id: str


class CallbackRequest(BaseModel):
    user_id: int | None = None
    course_interest: str
    preferred_time: str
    notes: str | None = None
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    country_code: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Please enter a valid name")
        return value.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Please enter your mobile number")

        if value.startswith("+"):
            value = value[1:]

        if not value.isdigit():
            raise ValueError("Please enter a valid mobile number")

        if len(value) < 7:
            raise ValueError("Mobile number is too short")

        if len(value) > 15:
            raise ValueError("Mobile number is too long")

        return value


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str