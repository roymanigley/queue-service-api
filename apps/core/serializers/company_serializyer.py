from rest_framework import serializers

from apps.authentication.models import UserProfile
from apps.core.models import Company
from config.middlewares import get_current_user


class CompanyFilterSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ('organization',)

    def create(self, validated_data: dict) -> Company:
        user: UserProfile = get_current_user()
        validated_data['organization'] = user.organization
        return super().create(validated_data)