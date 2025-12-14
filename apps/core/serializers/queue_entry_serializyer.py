from rest_framework import serializers

from apps.core.models import QueueEntry


class QueueEntryFilterSerializer(serializers.Serializer):
    queue_id = serializers.IntegerField(required=False)
    waiting_end_is_null = serializers.BooleanField(required=False)
    date = serializers.DateField(required=False)

class QueueEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = QueueEntry
        fields = '__all__'
