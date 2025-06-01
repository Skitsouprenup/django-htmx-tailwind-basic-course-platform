import smtplib
from email.mime.text import MIMEText

import config

subject = "Email Subject"
body = "This is the body of the text message"
sender = config.get_email_env("EMAIL_HOST_USER")
password = config.get_email_env("EMAIL_HOST_PASSWORD")


def send_email(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")