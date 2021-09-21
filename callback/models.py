from django.db import models


class Queue(models.Model):
    some_data = models.CharField(max_length=255, default="")
    executed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

