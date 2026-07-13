# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta, timezone

# from utils.otp import generate_otp
# from email_service import send_otp_email
# from database import get_db
# from models import ChatbotUser
# from schemas import UserCreate, OTPVerify

# from database import get_db
# router = APIRouter()

# IST = timezone(timedelta(hours=5, minutes=30))

# @router.post("/register")
# def register_user(user: UserCreate, db: Session = Depends(get_db)):

#     existing_user = db.query(ChatbotUser).filter(
#         ChatbotUser.email == user.email
#     ).first()

#     # -----------------------------------------
#     # Existing User
#     # -----------------------------------------

#     if existing_user:
#         if user.country_code and not existing_user.country_code:
#             existing_user.country_code = user.country_code


#         if existing_user.email_verified:

#             return {
#                 "success": True,
#                 "existing_user": True,
#                 "verified": True,
#                 "message": "User already verified. Continue to chatbot."
#             }

#         otp = generate_otp()

#         existing_user.otp = otp
#         existing_user.otp_expiry = (
#             datetime.now(IST).replace(tzinfo=None)
#             + timedelta(minutes=5)
#         )

#         db.commit()
#         db.refresh(existing_user)

#         print("========= USER OTP DEBUG =========")
#         print("OTP:", otp)
#         print("Created At:", existing_user.created_at)
#         print("OTP Expiry:", existing_user.otp_expiry)
#         print("Country Code:", existing_user.country_code)
#         print("==================================")

#         send_otp_email(existing_user.email, otp)

#         return {
#             "success": True,
#             "existing_user": True,
#             "verified": False,
#             "message": "OTP resent."
#         }

#     # -----------------------------------------
#     # New User
#     # -----------------------------------------

#     otp = generate_otp()

#     otp_expiry = (
#         datetime.now(IST).replace(tzinfo=None)
#         + timedelta(minutes=10)
#     )

#     new_user = ChatbotUser(
#         name=user.name,
#         email=user.email,
#         phone=user.phone,
#         country_code=user.country_code,
#         role="user",
#         email_verified=False,
#         otp=otp,
#         otp_expiry=otp_expiry,
#         created_at=datetime.now(IST).replace(tzinfo=None)
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     print("AFTER DB SAVE:")
#     print(new_user.otp)
#     print(new_user.otp_expiry)
#     print(new_user.country_code)

#     send_otp_email(user.email, otp)

#     return {
#         "success": True,
#         "existing_user": False,
#         "verified": False,
#         "message": "OTP sent.",
#         "id": new_user.id
#     }


# # =====================================================
# # VERIFY OTP
# # =====================================================

# @router.post("/verify-otp")
# def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):

#     user = db.query(ChatbotUser).filter(
#         ChatbotUser.email == data.email
#     ).first()

#     if not user:
#         return {
#             "success": False,
#             "message": "User not found."
#         }

#     if user.otp != data.otp:
#         return {
#             "success": False,
#             "message": "Invalid OTP."
#         }

#     if user.otp_expiry is None:
#         return {
#             "success": False,
#             "message": "OTP not found."
#         }

#     current_time = datetime.now(IST).replace(tzinfo=None)

#     if current_time > user.otp_expiry:
#         return {
#             "success": False,
#             "message": "OTP expired."
#         }

#     user.email_verified = True
#     user.otp = None
#     user.otp_expiry = None

#     db.commit()

#     return {
#         "success": True,
#         "verified": True,
#         "message": "Email verified successfully."
#     }


# # =====================================================
# # CHATBOT ACCESS
# # =====================================================

# @router.get("/chatbot/{email}")
# def chatbot_access(email: str, db: Session = Depends(get_db)):

#     user = db.query(ChatbotUser).filter(
#         ChatbotUser.email == email
#     ).first()

#     if not user:
#         return {
#             "success": False,
#             "message": "User not found."
#         }

#     if not user.email_verified:
#         return {
#             "success": False,
#             "message": "Verify your email before accessing chatbot."
#         }

#     return {
#         "success": True,
#         "message": "Access granted.",
#         "user": {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "role": user.role
#         }
#     }


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from utils.otp import generate_otp
from email_service import send_otp_email
from database import get_db
from models import ChatbotUser
from schemas import UserCreate, OTPVerify

router = APIRouter()

IST = timezone(timedelta(hours=5, minutes=30))

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(ChatbotUser).filter(
        ChatbotUser.email == user.email
    ).first()

    # -----------------------------------------
    # Existing User
    # -----------------------------------------
    if existing_user:
        if user.country_code and not existing_user.country_code:
            existing_user.country_code = user.country_code
            db.commit() # FIX 1: Commit instantly when mutations occur

        # FIX 2: Raise 409 Conflict so React catches it and drops to the catch() block
        if existing_user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already exists"
            )

        # Regenerate OTP for existing unverified accounts
        otp = generate_otp()
        existing_user.otp = otp
        existing_user.otp_expiry = (
            datetime.now(IST).replace(tzinfo=None)
            + timedelta(minutes=5)
        )

        db.commit()
        db.refresh(existing_user)

        print("========= USER OTP DEBUG =========")
        print("OTP:", otp)
        print("==================================")

        send_otp_email(existing_user.email, otp)

        return {
            "success": True,
            "existing_user": True,
            "verified": False,
            "message": "OTP resent."
        }

    # -----------------------------------------
    # New User
    # -----------------------------------------
    otp = generate_otp()
    otp_expiry = (
        datetime.now(IST).replace(tzinfo=None)
        + timedelta(minutes=10)
    )

    new_user = ChatbotUser(
        name=user.name,
        email=user.email,
        phone=user.phone,
        country_code=user.country_code,
        role="user",
        email_verified=False,
        otp=otp,
        otp_expiry=otp_expiry,
        created_at=datetime.now(IST).replace(tzinfo=None)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_otp_email(user.email, otp)

    return {
        "success": True,
        "existing_user": False,
        "verified": False,
        "message": "OTP sent.",
        "id": new_user.id
    }


# =====================================================
# VERIFY OTP
# =====================================================
@router.post("/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):

    user = db.query(ChatbotUser).filter(
        ChatbotUser.email == data.email
    ).first()

    # FIX 3: Convert raw dictionary returns to standard 400/404 HTTP errors
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if user.otp != data.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP.")

    if user.otp_expiry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found.")

    current_time = datetime.now(IST).replace(tzinfo=None)

    if current_time > user.otp_expiry:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired.")

    user.email_verified = True
    user.otp = None
    user.otp_expiry = None

    db.commit()

    return {
        "success": True,
        "verified": True,
        "message": "Email verified successfully."
    }


# =====================================================
# CHATBOT ACCESS
# =====================================================
@router.get("/chatbot/{email}")
def chatbot_access(email: str, db: Session = Depends(get_db)):

    user = db.query(ChatbotUser).filter(
        ChatbotUser.email == email
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if not user.email_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verify your email before accessing chatbot.")

    return {
        "success": True,
        "message": "Access granted.",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }