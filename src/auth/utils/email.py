import smtplib
from email.message import EmailMessage
from config.config import app_settings

def send_email(to: str, subject: str, body: str) -> None:
    """
    Send an email.

    Args:
        to (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body of the email.

    Returns:
        None
    """
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = app_settings.get('email_from')
    msg['To'] = to

    with smtplib.SMTP(app_settings.get('email_host'), app_settings.get('email_port')) as server:
        server.starttls()
        server.login(app_settings.get('email_from'), app_settings.get('email_password'))
        server.send_message(msg)

def send_activation_email(to: str, token: str) -> None:
    """
    Send an activation email.

    Args:
        to (str): The email address of the recipient.
        token (str): The activation token.

    Returns:
        None
    """
    activation_url = f"{app_settings.get('app_url')}/auth/activate/{token}"
    body = f"Hello {to},\n\n Click the link below to activate your account: {activation_url}"
    send_email(to, f"Activate your {app_settings.get('app_name')} account", body)