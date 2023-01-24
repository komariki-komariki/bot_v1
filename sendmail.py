import email, smtplib, ssl
import os

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tokens import yandex_bot


def sendmail(file, adress):
    subject = "Заключение"
    body = f"Заключение по {str(file)}.\n С уважением, робот-помощник"
    sender_email = "ilya@komarov-7.ru"
    receiver_email = adress
    password = yandex_bot
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    filename = file
    docx = MIMEApplication(open(filename, 'rb').read())
    docx.add_header('Content-Disposition', 'attachment', filename= filename)
    message.attach(docx)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.yandex.ru', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        print("Письмо отправлено")
        os.remove(file)
