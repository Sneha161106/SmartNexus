import pandas as pd
import time

def show_dashboard():

    while True:

        try:
            df = pd.read_csv("incident_log.csv")

            print("\n========= INCIDENT DASHBOARD =========\n")

            print(df.tail(10))

        except:
            print("No incidents yet...")

        time.sleep(5)


if __name__ == "__main__":
    show_dashboard()