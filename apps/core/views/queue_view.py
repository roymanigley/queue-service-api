from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from apps.authentication.models import UserProfile
from apps.core.models import Queue
from apps.core.permissions import QueuePermission
from apps.core.serializers.queue_serializyer import QueueSerializer, QueueFilterSerializer
from apps.shared.permissions import StrictModelPermission
from config.middlewares import get_current_user


@extend_schema(tags=['Queue'])
class QueueViewSet(ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = [StrictModelPermission, QueuePermission]

    @extend_schema('Update Queue')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema('List Queues', parameters=[
        OpenApiParameter(name='company_id', required=False, type=int, description='The ID of the company'),
    ])
    def list(self, request, *args, **kwargs):
        serializer = QueueFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        queryset = self.get_queryset()
        if company_id := data.get('company_id'):
            queryset = queryset.filter(company_id=company_id)
        queryset = self.paginate_queryset(queryset)
        return self.get_paginated_response(queryset)

    @extend_schema('Find Queue By ID')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema('Update Queue Partial')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema('Create Queue')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema('Delete Queue')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
        
    def get_queryset(self):
        user: UserProfile = get_current_user()
        return super().get_queryset().filter(company__organization=user.organization)

