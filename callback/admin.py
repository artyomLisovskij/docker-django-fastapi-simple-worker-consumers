from django.contrib import admin
from callback.models import (
    Queue
)


class QueueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Queue._meta.get_fields()]


admin.site.register(Queue, QueueAdmin)

