from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from apps.authentication.models import UserProfile, Organization


@admin.register(Organization)
class CustomOrganization(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'organization',)
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': ('organization',)}),
    )
    search_fields = ('username',)
    list_filter = ('organization',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'user', 'expire_date']
    readonly_fields = ['session_key', 'session_data', 'expire_date']

    def user(self, obj):
        from django.contrib.auth.models import User
        try:
            uid = obj.get_decoded().get('_auth_user_id')
            return User.objects.get(pk=uid)
        except:
            return None