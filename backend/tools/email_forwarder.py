import smtplib
import os
from email.message import EmailMessage

def forward_email(subject, destination):
    email_user = os.getenv("EMAIL_ADDRESS")
    email_pass = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg.set_content("Encaminhado automaticamente com base no assunto.")
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = destination

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)

    return { "status": "sent", "to": destination, "subject": subject }
