
# django fastapi project with multiple consumers and one worker example

### run locally
```
$ uvicorn mysite.asgi:fastapp --reload #fastapi
...
$ ./manage.py collectstatic --noinput  # generate static files for django admin
...
$ uvicorn mysite.asgi:application --port 8001 --reload  # Django
...

```
* http://localhost:8000/ -- frontend
* http://localhost:8000/api/docs  -- fastapi
* http://localhost:8001/admin -- django

### run using docker-compose (recommended)

```
docker ps

#look for app container id and paste instead of 9f. Note: migrate makes automaticall on every rebuild
docker exec -ti 9f python3 manage.py migrate

#to rebuild
docker-compose up -d --build

# create superuser
docker exec -ti 9f python3 manage.py createsuperuser

# or:
docker exec -ti 9f python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
```

