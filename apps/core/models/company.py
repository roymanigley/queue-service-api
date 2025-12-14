from django.db import models

from apps.core.models.abstracts import AuditableModel


class Company(AuditableModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey('authentication.Organization', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
