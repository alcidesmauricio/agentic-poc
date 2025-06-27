import imaplib, email, os
from datetime import datetime
from email.header import decode_header

def decode_mime_words(header_value):
    decoded_parts = decode_header(header_value)
    result = ''
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(enc or 'utf-8', errors='replace')
        else:
            result += part
    return result

def read_imap_emails():
    email_user = os.getenv("EMAIL_ADDRESS")
    email_pass = os.getenv("EMAIL_PASSWORD")

    domain = email_user.split("@")[-1]
    imap_host = "imap.gmail.com" if "gmail" in domain else "outlook.office365.com"

    if not email_user or not email_pass:
        raise ValueError("EMAIL_ADDRESS e EMAIL_PASSWORD devem estar definidos no .env")

    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    today = datetime.today().strftime("%d-%b-%Y")
    status, data = mail.search(None, f'(UNSEEN SINCE {today})')
    email_ids = data[0].split()

    result = []

    for eid in email_ids[:5]:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = email.message_from_bytes(msg_data[0][1])

        subject = decode_mime_words(raw_email["Subject"])
        from_ = raw_email["From"]

        result.append({"from": from_, "subject": subject})

    mail.logout()
    return result



#guedes teste