import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

class EmailSender:
    def __init__(self, smtp_server, port, username, password):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, recipient, subject, body, attachments=None):
        msg = MIMEMultipart()
        msg['From'] = formataddr(("", self.username))
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        # Attachments not implemented yet
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return True, None
        except Exception as e:
            return False, str(e)

    def send_bulk(self, recipients, subject, body, attachments=None):
        results = []
        for recipient in recipients:
            success, error = self.send_email(recipient, subject, body, attachments)
            results.append({'recipient': recipient, 'success': success, 'error': error})
        return results 