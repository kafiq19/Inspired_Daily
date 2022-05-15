import imghdr
import time
import schedule
import datetime
import smtplib
from email.message import EmailMessage

class Daily_Quote:

    def __init__(self):
        self.load_data()
        self.select_message()
        self.notification()

def load_data(self):
    csv_data = pd.read_csv('quotes.csv', names=['author', 'quote','ka', 'sch','tags'], dtype={'quote': str})
    csv_data['sch'] = pd.to_datetime(csv_data['sch'], format='%m/%d/%Y')

def select_message(self):
    msg = csv_data.loc[random.randint(0,len(csv_data.index))]

def notification(self):
    #creates a notification email
    today = datetime.date.today()
    gmail_user = 'khalfeen1@gmail.com'
    gmail_password = 'B@l@nc3G2021'
    recipient = ['tha_realist1990@hotmail.com']
    
    msg = EmailMessage()
    msg['Subject'] = 'Daily Quote: ' + str(today)
    msg['From'] = gmail_user 
    msg['To'] = recipient 
    msg.set_content(f'{msg.quote} \n {msg.author}')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(gmail_user, gmail_password) 
        smtp.send_message(msg)

    print("Successfully sent notification email")

if __name__ == "__main__":
    schedule.every().day.at("19:00").do(Daily_Quote)
    schedule.every(10).minutes.do(Daily_Quote)

    while 1:
        schedule.run_pending()
        time.sleep(1)