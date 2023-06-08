import smtplib, ssl
from smtplib import SMTPAuthenticationError

from email.mime.text import MIMEText


# Send email 
def send_email(email, password, bcc_recipients, subject, body) -> bool:
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email
    try:
        # Set up connection to gmail's SMTP server (TLS)
        TLS_PORT = 587
        with smtplib.SMTP('smtp.gmail.com', TLS_PORT) as smtp_server:
            # Certificate verification, hostname verification
            context = ssl.create_default_context()
            smtp_server.starttls(context=context)
            # Login using email and app password
            smtp_server.login(email, password)
            smtp_server.sendmail(email, bcc_recipients, msg.as_string())
        return True
    except:
        # Failed to send
        return False


if __name__ == '__main__':
    send_email('byung806@gmail.com', input(), ['smcs2025.cbtsoftware@gmail.com', 'bryandragonyayyayyay@gmail.com'], 'Test', 'Hello this worked')