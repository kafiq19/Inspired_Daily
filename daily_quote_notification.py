import os
import random
import imghdr
import time
import datetime
import smtplib
import pandas as pd
from email.message import EmailMessage

class Daily_Quote:

    def __init__(self):
        self.csv_data = ''
        self.quote = ''

    def load_data(self):
        self.csv_data = pd.read_csv('quotes.csv', names=['author', 'quote','ka', 'sch','tags'], dtype={'quote': str})
        self.csv_data['sch'] = pd.to_datetime(self.csv_data['sch'], format='%m/%d/%Y')
    
    def select_message(self):
        self.quote_ = self.csv_data.loc[random.randint(0,len(self.csv_data.index))]

    def notification(self):
        #creates a notification email
        today = datetime.date.today()
        gmail_user = 'khalfeen1@gmail.com'
        gmail_password = '82O1nNH6sFdjUXzw'
        recipient = ['tha_realist1990@hotmail.com', 'krarfeen@gmail.com', 'andreadprm@gmail.com']
        
        msg = EmailMessage()
        msg['Subject'] = 'Daily Quote: ' + str(today)
        msg['From'] = gmail_user 
        msg['To'] = recipient 
        msg.set_content(f'{self.quote_.quote} \n {self.quote_.author} \n\n inspired-daily.com')
        
        with smtplib.SMTP('smtp-relay.sendinblue.com', 587) as smtp:
            smtp.login(gmail_user, gmail_password) 
            smtp.send_message(msg)
    
        print("Successfully sent notification email")

if __name__ == "__main__":
    sesh = Daily_Quote()
    sesh.load_data()
    sesh.select_message()
    sesh.notification()