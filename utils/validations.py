from utils.exception_handler import ValidationException
from fastapi import HTTPException

def validate_message(message: str):

    if not message.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid question."
        )

    if len(message) > 300:
        raise HTTPException(
            status_code=400,
            detail="Question cannot exceed 300 characters."
        )

    return True