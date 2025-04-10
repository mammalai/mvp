import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

class MailGateway:
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    ENABLE_MAILS = os.environ.get("ENABLE_MAILS", "").lower() in ("true", "1", "yes") and SENDGRID_API_KEY is not None
    if SENDGRID_API_KEY:
        sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)

    @classmethod
    def send(cls, from_email: str, to_emails: list, subject: str, html_content: str):
        print(f"Sending password reset email to {from_email}")

        if not MailGateway.ENABLE_MAILS:
            return

        message = Mail(
            from_email=f'info@{os.environ.get("DOMAIN_NAME")}',
            to_emails=to_emails,
            subject=subject,
            html_content=html_content
        )

        MailGateway.sendgrid_client.send(message)
