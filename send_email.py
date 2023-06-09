import smtplib, ssl
from smtplib import SMTPAuthenticationError

from email.mime.text import MIMEText


# Send email 
def send_email(email, password, bcc_recipients, subject, body) -> bool:
    if not email or not password or not bcc_recipients:
        return False, 'Email failed to send. Please fill in the username, app password, and add at least 1 recipient.'
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
        return True, 'Email sent!'
    except TimeoutError:
        # Socket connection failed
        return False, 'Email failed to send. Please make sure you\'re connected to the internet.'
    except SMTPAuthenticationError:
        return False, 'Email failed to send. Incorrect username or password.'
    except:
        return False, 'Email failed to send.'
