# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import time
from xadmin.models import UserWidget, UserSettings

class Command(BaseCommand):

    def handle(self, *attrs, **options):
        while True:
            UserWidget.objects.all().delete()
            UserSettings.objects.all().delete()
            time.sleep(60*5)
        