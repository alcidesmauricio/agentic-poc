import os
from backend.tools.email_forwarder import forward_email

def decide_and_forward(emails):
    responses = []
    for mail in emails:
        subject = mail["subject"].lower()
        if "assumption" in subject or "trabalho" in subject:
            res = forward_email(subject, os.getenv("EMAIL_WORK_DEST"))
        else:
            res = forward_email(subject, os.getenv("EMAIL_PERSONAL_DEST"))
        responses.append(res)
    return responses
