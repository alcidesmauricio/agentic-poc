import imaplib
import email
import os
from email.header import decode_header

def fetch_latest_email():
    imap_host = "outlook.office365.com"
    email_user = os.getenv("EMAIL_ADDRESS")
    email_pass = os.getenv("EMAIL_PASSWORD")

    if not email_user or not email_pass:
        raise ValueError("EMAIL_ADDRESS e EMAIL_PASSWORD devem estar definidos no .env")

    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()

    result = []
    for email_id in email_ids[:5]:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        from_ = msg.get("From")
        result.append({"from": from_, "subject": subject})

    mail.logout()
    return result