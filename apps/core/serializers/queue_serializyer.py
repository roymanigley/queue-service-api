from rest_framework import serializers

from apps.core.models import Queue


class QueueFilterSerializer(serializers.Serializer):
    company_id = serializers.IntegerField(required=False)

class QueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Queue
        fields = '__all__'
