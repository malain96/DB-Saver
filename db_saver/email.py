import smtplib
import ssl
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Config


class Email:

    # Generate send an email
    @staticmethod
    def send(receiver_email, message):
        port = Config.PORT  # For SSL
        smtp_server = Config.SMTP_SERVER
        sender_email = Config.EMAIL  # Enter your address
        password = Config.PASSWORD

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()

    # Generate the email error message
    @staticmethod
    def error_message(email, content):
        msg = MIMEMultipart()
        msg['From'] = 'DB-Saver'
        msg['To'] = email
        msg['Subject'] = 'Backup - Failed'

        dt = datetime.datetime.now()
        body = 'An error occurred while backing up your databases the ' + dt.strftime('%m/%d/%Y at %H:%M:%S') + '.\n' \
            'The error message was the following:\n' + content
        msg.attach(MIMEText(body, 'plain'))

        return msg.as_string()

    # Generate the email success message
    @staticmethod
    def success_message(email):
        msg = MIMEMultipart()
        msg['From'] = 'DB-Saver'
        msg['To'] = email
        msg['Subject'] = 'Backup - Successful'

        dt = datetime.datetime.now()
        body = 'The backup of your databases the ' + dt.strftime('%m/%d/%Y at %H:%M:%S') + ' was successful!\n' \
            'The files are available in the "/storage/backups" folder of DB-Saver.'
        msg.attach(MIMEText(body, 'plain'))

        return msg.as_string()
