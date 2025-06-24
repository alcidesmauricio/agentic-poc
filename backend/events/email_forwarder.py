import smtplib, os
from email.mime.text import MIMEText

async def forward_email(original_from, subject, to_email):
    body = f"E-mail original de: {original_from}\nAssunto: {subject}"

    msg = MIMEText(body)
    msg["Subject"] = f"[FWD] {subject}"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)

    print(f"E-mail encaminhado para {to_email}")