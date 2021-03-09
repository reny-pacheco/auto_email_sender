import smtplib
import os
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()

from_me = os.environ.get('MY_EMAIL')
pwd = os.environ.get('MY_GMAIL_PASS')


#getting the contact list from teh text file
def get_contacts(filename):
    receiver = []
    emails = []

    with open(filename, mode='r', encoding='utf-8') as contacts:
        for contact in contacts:
            receiver.append(contact.split()[0])
            emails.append(contact.split()[1])
        return receiver, emails


#reading the text file to be send
def read_txt_msg(filename):
    with open(filename, mode='r', encoding='utf-8') as text_file:
        text_file_content = text_file.read()
    return Template(text_file_content)


receivers, emails = get_contacts('contacts.txt')

#sending emails to recievers
try:
    for recvr, email in zip(receivers, emails):
        message_template = read_txt_msg('message.txt')
        s.login(from_me, pwd)

        msg = MIMEMultipart()

        message = message_template.substitute(NAME=recvr)

        msg['From'] = from_me
        msg['To'] = email
        msg['Subject'] = message

        msg.attach(MIMEText(message, 'plain'))

        s.send_message(msg)

        del msg

        print(f'Email sent to {recvr}')
        time.sleep(2)

except Exception as e:
    print(e)
finally:
    s.quit()

# Reny Pacheco

