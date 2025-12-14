from django.db import models

from apps.core.models.abstracts import AuditableModel


class QueueEntry(AuditableModel):
    queue = models.ForeignKey('Queue', on_delete=models.CASCADE)
    description = models.TextField()
    start_waiting = models.DateTimeField(auto_now_add=True)
    end_waiting = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.queue} - [{self.start_waiting} - {self.end_waiting or ""}]'

    class Meta:
        ordering = ['start_waiting']
