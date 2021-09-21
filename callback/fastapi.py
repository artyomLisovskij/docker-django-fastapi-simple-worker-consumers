from fastapi import APIRouter
from callback.models import (
    Queue
)
import json
import requests
from django.db import transaction

router = APIRouter()

# TODO: move to environment
INTERNAL_CRON_API_KEY = 'testpassword'
WSIFY_URL = 'http://wsify:4040'

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
        all_queued_items = Queue.objects.select_for_update().filter(executed=False)
        with transaction.atomic():
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
        return {"status": "ok"}
    else:
        return {"status": "error"}
