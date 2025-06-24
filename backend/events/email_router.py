import smtplib
import os
from email.message import EmailMessage

async def forward_to_work(email_data, summary):
    dest = os.getenv("EMAIL_WORK_DEST")
    msg = EmailMessage()
    msg["Subject"] = f"FWD: {email_data['subject']}"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = dest
    msg.set_content(f"Resumo:\n{summary}\n\nOriginal:\nDe: {email_data['from']}\nAssunto: {email_data['subject']}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)
