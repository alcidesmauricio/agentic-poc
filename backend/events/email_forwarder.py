import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def forward_email(email_data, destination):
    msg = EmailMessage()
    msg["Subject"] = f"FWD: {email_data['subject']}"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = destination
    msg.set_content(email_data["body"])

    with smtplib.SMTP_SSL("smtp.office365.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)

