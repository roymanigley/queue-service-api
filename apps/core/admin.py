from django.contrib import admin

from apps.core import models

admin.site.register(models.Company)
admin.site.register(models.Queue)
admin.site.register(models.QueueEntry)
