import os
import time
import json
import random
import logging
import smtplib
import sqlite3
import datetime
import pandas as pd
from dotenv import load_dotenv
from email.message import EmailMessage

class Daily_Quote:

    def __init__(self):
        self.csv_data = ''
        self.quote = ''
        self.df_length = ''
        self.index = ''
        self.recipients = 'recipients.json'
        self.sql_file = './database/inspired_daily.db'
        self.sql_conn = ''
        self.logger_setup()

        #logic flow
        logging.info("Initialized Daily_Quote_Check, beginning work..")
        
        self.configure()
        self.load_data()

        if self.df_length:
            self.select_message()
            self.notification()

    def configure(self):
        load_dotenv()

        with open(self.recipients, 'r') as file:
            emails = json.load(file)

        self.recipients = emails.get('emails')

        logging.info(f'environment variables & recipient list loaded successfully.')

    def logger_setup(self):
        logging.basicConfig(
            filename='ID.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s')

    def load_csv_data(self):
        # note: superceded by sql datastructure (load_data())
        self.csv_data = pd.read_csv( \
            'quotes.csv', \
            names=['author', 'quote','ka', 'sch','tags'], \
            dtype={'quote': str})
        
        self.csv_data['sch'] = pd.to_datetime(self.csv_data['sch'], format='%m/%d/%Y')
        self.df_length = len(self.csv_data.index) - 1

        logging.info(f'csv loaded, -{self.df_length} records')

    def load_data(self):
        conn = sqlite3.connect(self.sql_file)
        self.sql_conn = conn.cursor()
        
        self.sql_conn.execute('SELECT COUNT(*) FROM mytable')
        row_count = self.sql_conn.fetchone()[0]
        self.df_length = row_count

        logging.info(f'sql loaded, -{self.df_length} records')
        
    def select_message_csv(self):
        self.quote_ = self.csv_data.loc[random.randint(0,len(self.csv_data.index))]

        if pd.isna(self.quote.author):
            self.quote.author = 'Unknown'

        if pd.isna(self.quote.quote):
            # log error, re-fetch quote
            logging.error(f'ERROR: quote at index {self.index} returns no quote.')
            self.select_message()
            logging.warning(f'Trying to fetch another quote..')

        self.sql_conn.close()

        logging.info(f'message selected: {self.index} : {self.quote}')

    def select_message(self):
        # select index for random quote
        self.index = random.randint(1,self.df_length)

        self.sql_conn.execute("SELECT * FROM mytable WHERE id = ?", (self.index,))
        self.quote = self.sql_conn.fetchone()
        
        logging.info(f'message selected: {self.index} : {self.quote[2]}')

    def notification(self):
        #creates a notification email
        today = datetime.date.today()
        gmail_user = os.getenv("gmail_user")
        gmail_password = os.getenv("gmail_password")
        recipient_def = ['info@khalfeenmedia.com'] #default
        recipient = self.recipients
        # recipient = [\
        #     'k.a@unb.ca', 'andreadprm@gmail.com', 'Mayakiao@gmail.com',\
        #     'tonerwarehouse1@yahoo.com', 'shazeedakhan27@gmail.com','anisaharfeen@gmail.com',\
        #     'yasmin_arfeen@hotmail.com', 'anshuk.chhibber@gmail.com','ara952@gmail.com'\
        #     ]
        # recipient = ['tha_realist1990@hotmail.com'] #dev
        
        msg = EmailMessage()
        msg['Subject'] = 'Your Dose of Daily Inspiration: ' + str(today)
        msg['From'] = f'Inspired Daily <{gmail_user}>'
        msg['To'] = recipient_def
        msg['Bcc'] = recipient
        #msg.set_content(f'"{self.quote[2]}" \n {self.quote[1]} \n\n inspired-daily.com')
        
        msg.set_content("""\
        <html>
            <head></head>
            <body>
                <h1 style="color: #4485b8; text-align: center; font-size: 30px">🐤Inspired Daily</h1>
                <p style="text-align: center;">Your Daily Source of Wisdom</p>
                <div class="container">
                  <div class="center">
                    <p style="text-align: center; font-style: bold; font-size: 40px">""" +self.quote[2]+"""</p>
                    <p style="text-align: center; font-style: italic; font-size: 30px">""" +self.quote[1]+"""</p>
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

if __name__ == "__main__":
    instance = Daily_Quote()

    # # introduce logic to send email again if failure
    # counter = 0
    # email_sent = False
    
    # while not email_sent and counter <= 10:

    #     try:
    #         instance = Daily_Quote()
    #         counter += 1
        
    #     except:
    #         logging.warning(f'Error completing notification on attempt {counter}. Retrying ..')

    #     else:
    #         email_set = True



# # working SSH command. Send from cmd directly. 
# scp -r "D:\OneDrive\Running\Utilities\inspired-daily\daily-inspired\Deta\Inspired_Daily" thief1432@192.168.2.21:/home/thief1432/Documents/
# pscp "D:\OneDrive\Running\Utilities\inspired-daily\daily-inspired\Deta\Inspired_Daily\daily_quote_notification.py" thief1432@192.168.2.21:/home/thief1432/Documents/Inspired-Daily

# # crontab linux: 
# 0 5 * * * /usr/bin/python3 /home/thief1432/Documents/Inspired-Daily/daily_quote_notification.py &> /home/thief1432/Documents/Inspired-Daily/scheduler.log

#  # test- cron jobs being executed && writing to file in directory
# * * * * * date >> /home/thief1432/Documents/Inspired_Daily/ID.log

#  # test- executing a python script
# * * * * * cd /home/thief1432/Documents/Inspired_Daily/ && python3 exe_test.py

#  # test- solution(Atmp=1)
# * * * * * cd /home/thief1432/Documents/Inspired_Daily/ && python3 daily_quote_notification.py


# ---
# nohup view:
# ps aux | grep 'python3 /home/thief1432/Documents/scheduler.py'

