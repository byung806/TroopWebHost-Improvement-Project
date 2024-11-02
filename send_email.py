import os
import smtplib
import ssl
from smtplib import SMTPAuthenticationError
from dotenv import dotenv_values

from email.mime.text import MIMEText


config = {
    **dotenv_values("env.default"),
    **dotenv_values(".env"),
    **os.environ,
}


# Send email
def send_email(
    email: str, password: str, bcc_recipients: list[str], subject: str, body: str
) -> (bool, str):
    if not email or not password or not bcc_recipients:
        return (
            False,
            "Email failed to send. Please fill in the username, app password, and add at least 1 recipient.",
        )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email
    try:
        # Set up connection to gmail's SMTP server (TLS)
        with smtplib.SMTP(config["SMTP_SERVER"], config["TLS_PORT"]) as smtp_server:
            # Certificate verification, hostname verification
            context = ssl.create_default_context()
            smtp_server.starttls(context=context)
            # Login using email and app password
            smtp_server.login(email, password)
            smtp_server.sendmail(email, bcc_recipients, msg.as_string())
        return True, "Email sent!"
    except TimeoutError:
        # Socket connection failed
        return (
            False,
            "Email failed to send. Please make sure you're connected to the internet.",
        )
    except SMTPAuthenticationError:
        return False, "Email failed to send. Incorrect username or password."
    except Exception as e:
        return False, f"Email failed to send: {e}"


if __name__ == "__main__":
    sent, result_str = send_email(
        "email_address@example.com",
        "my_password",
        ["example_email_2@example.com"],
        "My Test Email",
        "Hello!\nThis is a test email\n",
    )
    assert sent is True
    assert result_str == "Email sent!"
