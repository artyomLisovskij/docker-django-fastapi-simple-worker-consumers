from fastapi import APIRouter
from callback.models import (
    Queue
)
from redis import Redis
import requests
from django.db import transaction
from dotenv import dotenv_values

redis = Redis(host="redis", port=6379)
redis.set('locked', 0)
router = APIRouter()

config = dotenv_values(".env")
INTERNAL_CRON_API_KEY = config["INTERNAL_CRON_API_KEY"]
WSIFY_URL = config["WSIFY_URL"]

# checker for wsify, is user allowed to connect
# allow all
@router.post("/check/", include_in_schema=False)
def check():
    return {"status": "ok"}

@router.get("/api/new_task/", include_in_schema=False)
def new_task(some_data: str = ''):
    queue_item = Queue()
    queue_item.some_data = some_data
    queue_item.save()
    return {"status": "ok", "channel": queue_item.id}
    

@router.get("/worker_run/", include_in_schema=False)
def worker_run(call_key: str = ''):
    if call_key == INTERNAL_CRON_API_KEY:
        # avoid worker run twice
        if redis.get('locked') == 1:
            return {"status": "locked"}
        else:
            redis.set('locked', 1)
            all_queued_items = Queue.objects.select_for_update().filter(executed=False)
            with transaction.atomic():
                try:
                    for queue_item in all_queued_items:
                        queue_item.executed = True
                        # do some stuff
                        queue_item.some_data = queue_item.some_data.upper()
                        queue_item.save()
                        result = {
                            "payload": {
                                "data": queue_item.some_data,
                                "completed": queue_item.updated.strftime("%m/%d/%Y, %H:%M:%S"),
                                "created": queue_item.created.strftime("%m/%d/%Y, %H:%M:%S"),
                                "executed": queue_item.executed
                            },
                            "channel": str(queue_item.id)
                        }
                        print(result)
                        requests.post(WSIFY_URL + '/publish' , json=result)
                except Exception as e:
                    print(e)
                    return {"status": "failed"}
            redis.set('locked', 0)
            return {"status": "ok"}
    else:
        return {"status": "error"}
