import smtplib 
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# this is used to load the variables that have been stored in the .env files
load_dotenv("virtual-assistant-sophia/.env") 

def sendEmail(mail_package):
    """This function accepts a dictionary as its input. The dictionary contains the receiver's name which will be mapped to its email address 
    (for now by an environment variable, later my personal database will be set up), the email subject, and the content.
    the fucntion logs into my email account and sends the email.
    """
    try:
        email = EmailMessage()
        name = mail_package["recipient_name"]
        email['To'] = os.getenv(name)
        email['Subject'] = mail_package["Subject"]
        email['From'] = os.getenv("username")
        email.set_content(mail_package["content"])


        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(os.getenv("username"), os.getenv("password"))
        s.send_message(email)
        s.close()

        return "Email has been sent"

    except Exception as e:
        print(e)
        return "Sorry, I'm unable to send the message at this time"


