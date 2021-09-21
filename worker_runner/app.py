import requests
import time
from dotenv import dotenv_values

config = dotenv_values(".env")
INTERNAL_CRON_API_KEY = config["INTERNAL_CRON_API_KEY"]

if __name__ == "__main__":
    while True:
        try:
            requests.get(
                "http://api:8000/worker_run/?call_key=" + INTERNAL_CRON_API_KEY
            )
        except Exception as e:
            print(e)
        time.sleep(1)
