import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read values safely
EMAIL = os.getenv("EMAIL_ADDRESS", "").strip()
PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip()

SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

# Debug (Safe)
print("========== EMAIL CONFIG ==========")
print(f"EMAIL       : '{EMAIL}'")
print(f"SMTP HOST   : '{SMTP_HOST}'")
print(f"SMTP PORT   : {SMTP_PORT}")
print(f"PASSWORD LEN: {len(PASSWORD)}")
print("==================================")


def send_otp_email(receiver_email: str, otp: str):
    """
    Sends OTP email using Hostinger SMTP.
    """

    if not EMAIL:
        raise ValueError("EMAIL_ADDRESS is missing in .env")

    if not PASSWORD:
        raise ValueError("EMAIL_PASSWORD is missing in .env")

    if not SMTP_HOST:
        raise ValueError("SMTP_HOST is missing in .env")

    msg = MIMEText(
        f"""
Hello,

Your verification code is:

{otp}

Please enter this OTP to verify your email.

This OTP will expire in 5 minutes.

Regards,
SwiftIntelli Team
"""
    )

    msg["Subject"] = "Email Verification"
    msg["From"] = EMAIL
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as server:

            print("Connecting to SMTP server...")

            server.login(EMAIL, PASSWORD)

            print("SMTP Login Successful.")

            server.send_message(msg)

            print(f"OTP email sent successfully to {receiver_email}")

    except smtplib.SMTPAuthenticationError as e:
        print("\nSMTP Authentication Failed")
        print("Check your email address and password.")
        print(e)
        raise

    except smtplib.SMTPConnectError as e:
        print("\nUnable to connect to SMTP server.")
        print(e)
        raise

    except Exception as e:
        print("\nUnexpected email error:")
        print(e)
        raise