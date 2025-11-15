from math import log
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import os

from app.core.config import get_config
from app.core.logger import get_logger


def send_email(
    to_emails: list[str],
    subject: str,
    body_text: str = "",
    body_html: str = None,
    attachments: list[str] = None,
):
    conf = get_config()
    logger = get_logger()
    sender_email = conf.smtp_sender_email
    app_password = conf.smtp_app_password

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject
    msg["From"] = formataddr(("Event Booker", sender_email))


    # Add plain text
    if body_text:
        msg.attach(MIMEText(body_text, "plain"))

    # Add HTML version
    if body_html:
        msg.attach(MIMEText(body_html, "html"))

    # Add attachments (if any)
    if attachments:
        for file_path in attachments:
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(file_path)}"',
                )
                msg.attach(part)
            else:
                print(f"⚠️ Warning: File not found - {file_path}")

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_emails, msg.as_string())
        logger.info("email sent successfully")
    except Exception as e:
        logger.error(msg=f"[EMAIL SMTP ERROR] error : {str(e)}")

