import time
from backend.events.email_reader import read_outlook_emails
from backend.actions.email_decision import decide_and_forward
from backend.agent.fsm.email_fsm import EmailStateMachine, EmailFSMState

def run_email_fsm():
    fsm = EmailStateMachine()

    fsm.transition(EmailFSMState.READING)
    emails = read_outlook_emails()

    if not emails:
        print("Nenhum email novo.")
        return

    fsm.transition(EmailFSMState.DECIDING)
    print(f"Analisando {len(emails)} emails...")

    fsm.transition(EmailFSMState.FORWARDING)
    result = decide_and_forward(emails)

    fsm.transition(EmailFSMState.DONE)
    print(f"{len(result)} emails processados.")

if __name__ == "__main__":
    run_email_fsm()
