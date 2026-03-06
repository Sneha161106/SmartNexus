import datetime
import csv
import os

LOG_FILE = "incident_log.csv"

def log_incident(event, score):

    time = datetime.datetime.now().strftime("%H:%M:%S")

    row = [time, event, score]

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Time", "Event", "ThreatScore"])

        writer.writerow(row)

    print("Logged:", row)