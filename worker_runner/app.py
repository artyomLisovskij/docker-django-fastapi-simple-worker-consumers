import requests
import time

INTERNAL_CRON_API_KEY = 'testpassword'

if __name__ == "__main__":
    while True:
        try:
            requests.get(
                "http://api:8000/worker_run/?call_key=" + INTERNAL_CRON_API_KEY
            )
        except Exception as e:
            print(e)
        time.sleep(1)
