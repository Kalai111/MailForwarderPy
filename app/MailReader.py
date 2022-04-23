import imaplib
import traceback
from MailSender import MailSender

class MailReader():
    __inst = None

    @staticmethod
    def getInstance():

        """Static Access Method"""
        if MailReader.__inst == None:
            MailReader()
        return MailReader.__inst

    def __init__(self):
        self.host = 'outlook.office365.com'
        """virtual private constructor"""
        if MailReader.__inst != None:
            raise Exception ("MailReader is a singleton class !")
        else:
            MailReader.__inst = self


    def retryOnFail(retryCount):
        def inner(callback):
            def wrapper(*args, **kwargs):
                execCount = 0
                while True:
                    try:
                        callback(*args, **kwargs)
                        break
                    except:
                        traceback.print_exc()
                        print("Attempts {}".format(execCount))
                        if execCount > retryCount:
                            print("Max attempts reached !!!")
                            break
                        execCount += 1
            return wrapper
        return inner

    def connect(self, email, password):
        print("{} Logging in .... ".format(email))
        self.imap = imaplib.IMAP4_SSL(self.host)
        self.imap.login(email, password)

    def disconnect(self):
        self.imap.close()
        self.imap.logout()

    def moveEmail(self, num):
        #self.imap.store(num, '+FLAGS', '\SEEN')  # Mark as read
        print("Moving Email num ", num)
        self.imap.create('INBOX.myInbox')
        self.imap.copy(num, 'INBOX.myInbox')
        self.imap.store(num, '+FLAGS', '\Deleted')
        self.imap.expunge()

    def processMailbox(self):
        emails = list()
        mailboxes = ["Inbox", "Junk"]
        for mailbox in mailboxes:
            print("Reading from {} ...".format(mailbox))
            self.imap.select(mailbox)
            respose_code, message_numbers_raw = self.imap.search(None, 'ALL')
            for num in message_numbers_raw[0].split():
                respose_code, data = self.imap.fetch(num, '(RFC822)')
                print('Message: {0}\n'.format(num))
                MailSender.getInstance().sendEmail(data[0][1])
                self.moveEmail(num)

    @retryOnFail(3)
    def processEmail(self, email, password):
        self.connect(email, password)
        self.processMailbox()
        self.disconnect()

