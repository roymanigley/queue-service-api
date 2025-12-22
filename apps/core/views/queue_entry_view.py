import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.viewsets import ModelViewSet

from apps.authentication.models import UserProfile
from apps.core.models import QueueEntry
from apps.core.permissions import QueueEntryPermission
from apps.core.serializers.queue_entry_serializyer import QueueEntrySerializer, QueueEntryFilterSerializer
from apps.shared.permissions import StrictModelPermission
from config.middlewares import get_current_user


@extend_schema(tags=['Queue Entry'])
class QueueEntryViewSet(ModelViewSet):
    queryset = QueueEntry.objects.all()
    serializer_class = QueueEntrySerializer
    permission_classes = [StrictModelPermission, QueueEntryPermission]

    @extend_schema('Update Queue Entry')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema('List Queue Entry', parameters=[
        OpenApiParameter(name='queue_id', required=False, type=int, description='ID of the queue'),
        OpenApiParameter(name='date', required=False, type=datetime.date, description='Date of the queue entry', examples=[OpenApiExample('Date ISO Format', 'YYYY-mm-dd')]),
        OpenApiParameter(name='waiting_end_is_null', required=False, type=bool, description='Whether the waiting end is null'),
    ])
    def list(self, request, *args, **kwargs):
        serializer = QueueEntryFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        queryset = self.get_queryset()
        if queue_id := data.get('queue_id'):
            queryset = queryset.filter(queue_id=queue_id)
        if date := data.get('date'):
            queryset = queryset.filter(start_waiting=date)
        if data.get('waiting_end_is_null') is not None:
            print( data.get('waiting_end_is_null'))
            queryset = queryset.filter(end_waiting__isnull= data.get('waiting_end_is_null'))
            print(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema('Find Queue Entry By ID')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema('Update Queue Entry Partial')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema('Create Queue Entry')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema('Delete Queue Entry')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user: UserProfile = get_current_user()
        return super().get_queryset().filter(queue__company__organization=user.organization)
