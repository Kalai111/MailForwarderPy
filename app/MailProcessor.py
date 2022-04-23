from Config import *
from MailReader import MailReader
from MailSender import MailSender

class MailProcessor():
    __inst = None

    @staticmethod
    def getInstance():

        """Static Access Method"""
        if MailProcessor.__inst == None:
            MailProcessor()
        return MailProcessor.__inst

    def __init__(self):

        """virtual private constructor"""
        if MailProcessor.__inst != None:
            raise Exception ("MailProcessor is a singleton class !")
        else:
            MailProcessor.__inst = self


    def start(self):
        for email in CREDENTIAL:
            MailReader.getInstance().processEmail(email, CREDENTIAL[email])


