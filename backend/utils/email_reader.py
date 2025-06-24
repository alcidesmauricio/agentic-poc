import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("EMAIL_IMAP_HOST")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASSWORD")

def fetch_unread_emails():
    try:
        conn = imaplib.IMAP4_SSL(IMAP_HOST)
        conn.login(EMAIL_USER, EMAIL_PASS)
        conn.select("INBOX")
        result, data = conn.search(None, 'UNSEEN')

        emails = []

        for num in data[0].split():
            result, data = conn.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg["subject"]
            decoded_subject, encoding = decode_header(subject)[0]
            if isinstance(decoded_subject, bytes):
                subject = decoded_subject.decode(encoding or 'utf-8', errors='replace')

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        charset = part.get_content_charset() or 'utf-8'
                        try:
                            body += part.get_payload(decode=True).decode(charset, errors='replace')
                        except LookupError:
                            body += part.get_payload(decode=True).decode('utf-8', errors='replace')
                        break
            else:
                charset = msg.get_content_charset() or 'utf-8'
                try:
                    body = msg.get_payload(decode=True).decode(charset, errors='replace')
                except LookupError:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='replace')

            emails.append({ "subject": subject, "body": body })

        conn.logout()
        return emails
    except Exception as e:
        print(f"[Erro ao ler emails]: {e}")
        return []
