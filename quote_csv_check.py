import os
import time
import random
import smtplib
import logging
import datetime
import pandas as pd
from dotenv import load_dotenv
from email.message import EmailMessage

class Daily_Quote_Check:

    def __init__(self):
        self.csv_data = ''
        self.quote = ''
        self.df_length = ''
        self.index = ''
        self.logger_setup()

        #logic flow
        logging.info("Initialized Daily_Quote_Check, beginning work..")
        
        self.load_data()
        
        if self.df_length:
        
            for index, row in enumerate(range(1, self.df_length)):
        
                self.index = index
                self.select_message()
                self.print_quote()
                self.notification()

    def logger_setup(self):
        logging.basicConfig(filename='ID.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_data(self):
        self.csv_data = pd.read_csv( \
            'quotes.csv', skiprows=1, \
            names=['author', 'quote','ka', 'sch','tags'], \
            dtype={'quote': str})
        self.csv_data['sch'] = pd.to_datetime(self.csv_data['sch'], format='%m/%d/%Y')
        self.df_length = len(self.csv_data.index) - 1
        logging.info(f'Data loaded Successfully, there are {self.df_length} records.')
    
    def select_message(self):
        self.quote_ = self.csv_data.loc[self.index]
        #self.quote_ = self.csv_data.loc[random.randint(1,len(self.csv_data.index))]

        if pd.isna(self.quote_.author):
            self.quote_.author = 'Unknown'

        if pd.isna(self.quote_.quote):
            # log error, re-fetch quote

            logging.error(f'ERROR: quote at index {self.index} returns no quote.')

            pass

        logging.info(f'message selected: {self.index} : {self.quote}')

    def print_quote(self):
        print(f'{self.index} : {self.quote_.quote} by {self.quote_.author}')

    def notification(self):
        #creates a notification email
        today = datetime.date.today()
        #gmail_user = os.getenv("gmail_user")
        #gmail_password = os.getenv("gmail_password")
        # recipient_def = ['info@khalfeenmedia.com'] #default
        # recipient = ['k.a@unb.ca', 'andreadprm@gmail.com', 'Mayakiao@gmail.com', 'tonerwarehouse1@yahoo.com',\
        #              'shazeedakhan27@gmail.com',  'anisaharfeen@gmail.com', 'yasmin_arfeen@hotmail.com', 'anshuk.chhibber@gmail.com', 'ara952@gmail.com']
        # recipient = ['tha_realist1990@hotmail.com'] #dev
        
        msg = EmailMessage()
        msg['Subject'] = 'Your Dose of Daily Inspiration: ' + str(today)
        # msg['From'] = f'Inspired Daily <{gmail_user}>'
        # msg['To'] = recipient_def
        # msg['Bcc'] = recipient
        #msg.set_content(f'"{self.quote_.quote}" \n {self.quote_.author} \n\n inspired-daily.com')
        
        try:
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

        except Exception as e:
            import pdb; pdb.set_trace()

        # with smtplib.SMTP('smtp-relay.sendinblue.com', 587) as smtp:
        #     smtp.login(gmail_user, gmail_password) 
        #     smtp.send_message(msg)
    
        print("Successfully sent notification email")


if __name__ == "__main__":
    sesh = Daily_Quote_Check()


#implement logger
#save index number to log, analyze when fails