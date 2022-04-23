from MailProcessor import MailProcessor

# https://www.devdungeon.com/content/read-and-send-email-python

def Main():
    MailProcessor.getInstance().start()

if __name__ == "__main__":
    Main()