import os
import time
import random
import imghdr
import smtplib
import datetime
import pandas as pd
from dotenv import load_dotenv
from email.message import EmailMessage

class Daily_Quote:

    def __init__(self):
        self.csv_data = ''
        self.quote = ''

    def configure(self):
        load_dotenv()

    def load_data(self):
        self.csv_data = pd.read_csv('quotes.csv', names=['author', 'quote','ka', 'sch','tags'], dtype={'quote': str})
        self.csv_data['sch'] = pd.to_datetime(self.csv_data['sch'], format='%m/%d/%Y')
    
    def select_message(self):
        self.quote_ = self.csv_data.loc[random.randint(0,len(self.csv_data.index))]

    def notification(self):
        #creates a notification email
        today = datetime.date.today()
        gmail_user = os.getenv("gmail_user")
        gmail_password = os.getenv("gmail_password")
        recipient_def = ['info@khalfeenmedia.com'] #default
        recipient = ['k.a@unb.ca', 'andreadprm@gmail.com', 'Mayakiao@gmail.com', \
                    'tonerwarehouse1@yahoo.com', 'shazeedakhan27@gmail.com', \
                    'anisaharfeen@gmail.com', 'yasmin_arfeen@hotmail.com',\
                    'anshuk.chhibber@gmail.com', 'ara952@gmail.com']
        recipient = ['tha_realist1990@hotmail.com', 'gecewex275@qqhow.com'] #dev
        
        msg = EmailMessage()
        msg['Subject'] = 'Your Dose of Daily Inspiration: ' + str(today)
        msg['From'] = f'Inspired Daily <{gmail_user}>'
        msg['To'] = recipient_def
        msg['Bcc'] = recipient
        #msg.set_content(f'"{self.quote_.quote}" \n {self.quote_.author} \n\n inspired-daily.com')
        
        msg.set_content("""\
        <html>
            <head></head>
            <body>
                <h1 style="color: #4485b8; text-align: center; font-size: 30px">🐤Inspired Daily</h1>
                <p style="text-align: center;">Your Daily Source of Wisdom</p>
                <div class="container">
                  <div class="center">
                    <p style="text-align: center; font-style: bold; font-size: 40px">""" +self.quote_.quote+"""</p>
                    <p style="text-align: center; font-style: italic; font-size: 30px">""" +self.quote_.author+"""</p>
                  </div>
                </div>
                <p style="text-align: center;"><em>&copy; inspired-daily.com</em></p>
            </body>
        </html>
        """)

        with smtplib.SMTP('smtp-relay.sendinblue.com', 587) as smtp:
            smtp.login(gmail_user, gmail_password) 
            smtp.send_message(msg)
    
        print("Successfully sent notification email")

def main_app():
    sesh = Daily_Quote()
    sesh.configure()
    sesh.load_data()
    sesh.select_message()
    sesh.notification()  

if __name__ == "__main__":
    main_app()