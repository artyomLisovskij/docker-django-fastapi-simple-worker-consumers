# Simple persistent queue proccesing (multiple consumers, one worker)
List of used packages and technologies:
* `django` for ORM and admin
* `fastapi` for api and worker start
* `wsify` for websocket subscribes
* `postgresql` for persistent storage
* `redis` for locks
* `requests` for JSON RPC calls
* `uvicorn`, `asgi` for deploy
* `python3` for code
* `docker` for platform-independent run
* `websocket` for async subscribes
* `html`, `js` for frontend
* `nginx` as router
* `pgadmin` for raw DB administration (commented inside docker-compose)
## Description
User(`frontend` in this case) sends task to the backend(`api` service) by calling `/api/new_task/?some_data=` (it may be not user, any consumer). `api` service receives new task and stores it to the queue(`db`) and gives `id` of queued item to the user(into response). 

Frontend(in this case) subscribes to websocket-based channel(by `wsify` service) named by queued task ID to receive result of task processing.

Service `worker_runner` in background calls `api` service worker endpoint every second(usually developers use cron but than you'll get up to 1 minute delay). 

Before each call we lock(using `redis` service) worker to make it impossible to be called twice(or when one job is not done yet). `worker` just gets all of queued items one-by-one and do it's job. 

When queued item processed `worker` write result to the db and send to `wsify` using channel named by ID(`frontend` already subscribed to this channel). 

---

We need `django` service here just for two reasons:
* i like Django ORM and we can use ORM inside `fastapi` service.
* Django has great admin interface for DB

We use `db` service to store queue persistent.

We use select_for_update to avoid race conditions when `worker` process queue.

## Schema
frontend (new task request) -> api -> DB -> (response to frontend) -> (frontend subscribes to wsify and waiting for task result)

In background:

worker_runner (calls) -> api (check that lock may be acquired) -> redis -> (process queue item) -> DB (mark queue item as processed) -> (post result to ws) wsify ---> frontend (receives result of task processing)


## Motivation
I don't like `celery` because it's hard to manage and it's huge(too many options). If you need simple persistent queue with one worker(and also ws/api/swagger/admin/storage/..) this solution would be useful.

> I like to control everything by my side, so I created this. It's simple, easy manageable and it just works.


## Usage
Copy `example.env` to `.env` and change variables.
### Run locally(w/o docker-compose) -- for development
```
# run fastapi only
$ uvicorn mysite.asgi:fastapp --reload

# generate staticfiles for django
$ ./manage.py collectstatic --noinput  # generate static files for django admin

# run django only
$ uvicorn mysite.asgi:application --port 8001 --reload
```

### Run using docker-compose (recommended)
```
# Run
$ docker-compose up -d

# show all started containers
docker ps

# look for app container id and paste instead of <id>. Note: migrate makes automaticall on every api/app run
docker exec -ti <id> python3 manage.py migrate

# to rebuild(recompile containers' images and restart changed containers)
$ docker-compose up -d --build

# create superuser
$ docker exec -ti <id> python3 manage.py createsuperuser

# or:
docker exec -ti <id> python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
```

#### Links
* http://localhost:8000/ -- frontend
* http://localhost:8000/api/docs  -- fastapi Swagger docs
* http://localhost:8000/api/  -- fastapi endpoints
* http://localhost:8001/admin -- django