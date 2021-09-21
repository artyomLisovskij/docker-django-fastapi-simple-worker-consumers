from django.core.management.base import BaseCommand
from callback.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # you can execute your queue items from commands too, but there will be not fastapi environment.