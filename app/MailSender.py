import smtplib
from Config import *

class MailSender():
    __inst = None

    @staticmethod
    def getInstance():
        """Static Access Method"""
        if MailSender.__inst == None:
            MailSender()
        return MailSender.__inst

    def __init__(self):
        self.host = "smtp.office365.com"
        self.host = "smtp.gmail.com"
        """virtual private constructor"""
        if MailSender.__inst != None:
            raise Exception ("MailSender is a singleton class !")
        else:
            MailSender.__inst = self


    def connect(self, user, password):
        print("Sending email via user {}/{} ..".format(user, password))
        self.smtp = smtplib.SMTP(self.host, 587)
        self.smtp.starttls() # Secure the connection
        self.smtp.login(user, password)

    def getHeader(self):
        headers = f"From: {SENDER_EMAIL}\r\n"
        headers += f"To: {DESTINATION_EMAIL}\r\n"
        headers += f"Subject: FWD Mail from MailForwarderPy\r\n"
        headers + "\r\n"
        return headers.encode('utf-8')


    def sendEmail(self, emailContent):
        self.connect(SENDER_EMAIL, SENDER_PASSWORD)
        print("Sending Email to {} ...".format(DESTINATION_EMAIL))
        self.smtp.sendmail(SENDER_EMAIL, DESTINATION_EMAIL, (self.getHeader() + emailContent))
        self.disconnect()

    def disconnect(self):
        self.smtp.quit()