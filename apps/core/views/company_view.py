from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet

from apps.authentication.models import UserProfile
from apps.core.models import Company
from apps.core.serializers.company_serializyer import CompanySerializer, CompanyFilterSerializer
from apps.shared.permissions import StrictModelPermission
from config.middlewares import get_current_user


@extend_schema(tags=['Company'])
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [StrictModelPermission]

    @extend_schema('Update Company')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema('List Companies', parameters=[
        OpenApiParameter(name='search', required=False, type=str, description='Search term'),
    ])
    def list(self, request, *args, **kwargs):
        serializer = CompanyFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        queryset = self.get_queryset()
        if search := data.get('search'):
            queryset = queryset.filter(name__icontains=search)
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema('Find Company By ID')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema('Update Company Partial')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema('Create Company')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema('Delete Company')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user: UserProfile = get_current_user()
        return super().get_queryset().filter(organization=user.organization)
