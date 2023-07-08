import os
import datetime

log_file = "exe_test.log"

# Check if log file exists, create it if not
if not os.path.exists(log_file):
    with open(log_file, "w") as file:
        file.write("Log file created\n")

# Open log file in append mode
with open(log_file, "a") as file:
    # Get current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Append the date to the log file
    file.write(current_datetime + "\n")