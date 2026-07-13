from datetime import datetime, timezone, timedelta
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String
)

from database import Base


class ChatbotUser(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # User Details
    name = Column(
        String(255),
        nullable=True
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )

    password = Column(
        String(255),
        nullable=True
    )

    role = Column(
        String(50),
        nullable=False,
        default="user"
    )

    phone = Column(
        String(20),
        nullable=True
    )

    country_code = Column(
        String(10),
        nullable=True
    )

    # OTP
    otp = Column(
        String(10),
        nullable=True
    )

    otp_expiry = Column(
        DateTime,
        nullable=True
    )

    email_verified = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # MySQL automatically sets CURRENT_TIMESTAMP
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone(timedelta(hours=5, minutes=30))).replace(tzinfo=None),
        nullable=False
    )
    