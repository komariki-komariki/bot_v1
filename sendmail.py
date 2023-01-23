import email, smtplib, ssl
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tokens import rambler


def sendmail(file, adress):
    subject = "Заключение"
    body = f"Заключение по {str(file)}.\n С уважением, робот-помощник"
    sender_email = "sb.robot@ro.ru"
    receiver_email = adress
    password = rambler

    # Создание составного сообщения и установка заголовка
    message = MIMEMultipart()
    # from_name = "Илья Комаров"
    # from_email = "sb.robot@ro.ru"
    message["From"] = sender_email
    # message["From"] = "{} <{}>".format(from_name, from_email)
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Если у вас несколько получателей

    # Внесение тела письма
    message.attach(MIMEText(body, "plain"))

    filename = file  # В той же папке что и код

    # Открытие PDF файла в бинарном режиме
    with open(filename, "rb") as attachment:
        # Заголовок письма application/octet-stream
        # Почтовый клиент обычно может загрузить это автоматически в виде вложения
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Шифровка файла под ASCII символы для отправки по почте
    encoders.encode_base64(part)

    # Внесение заголовка в виде пара/ключ к части вложения
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Внесение вложения в сообщение и конвертация сообщения в строку
    message.attach(part)
    text = message.as_string()

    # Подключение к серверу при помощи безопасного контекста и отправка письма
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.rambler.ru', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        print("Письмо отправлено")
        # os.remove(file)