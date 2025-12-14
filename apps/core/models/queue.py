from django.db import models

from apps.core.models.abstracts import AuditableModel


class Queue(AuditableModel):
    name = models.CharField(max_length=255)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company.name}: {self.name}'

    class Meta:
        ordering = ('name',)
