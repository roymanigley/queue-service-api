from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.authentication import views

router = DefaultRouter()

urlpatterns = [
    path('accounts/', views.user_account, name='account'),
    path('csrf/', views.get_csrf_token, name='csrf'),
    path('login/', views.login_view),
    path('', include('rest_framework.urls')),
] + router.get_urls()