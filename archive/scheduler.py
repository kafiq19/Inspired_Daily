import schedule
import time
import subprocess

def run_daily_script():
    # Run the daily_quote_notification.py script
    subprocess.run(['python', 'daily_quote_notification.py'])

# Schedule the job to run every day at 5 am
schedule.every().day.at("05:00").do(run_daily_script)

while True:
    # Run the pending scheduled jobs
    schedule.run_pending()
    time.sleep(60)  # Sleep for 60 seconds before checking the schedule again