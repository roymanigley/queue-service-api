from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers import UserSerializer


@extend_schema('CSRF Token', tags=['General'], responses={204: None})
@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request: Request) -> Response:
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema('Current User', tags=['User'], responses=UserSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_account(request: Request, *args, **kwargs) -> Response:
    if request.user.is_authenticated:
        return Response(
            {
                'username': request.user.username,
                'permissions': request.user.get_all_permissions(),
            }
        )
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@require_POST
def login_view(request: Request) -> Response:
    user = authenticate(
        request=request,
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )
    if user is None:
        return JsonResponse(data={'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    login(request=request, user=user)
    return HttpResponseRedirect('/api/auth/accounts/')