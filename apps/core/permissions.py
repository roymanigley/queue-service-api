from django.shortcuts import get_object_or_404
from rest_framework import permissions

from apps.authentication.models import UserProfile
from apps.core.models import Queue, Company, QueueEntry


class QueuePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user: UserProfile = request.user
        company_id = request.data.get('company')
        if request.method in ['POST']:
            if company := get_object_or_404(Company, id=company_id):
                return company.organization_id == user.organization_id
        if request.method in ['PUT', 'PATCH']:
            company = Company.objects.filter(id=company_id).first()
            if company is None or company.organization_id == user.organization_id:
                return True
        if request.method in ['GET', 'DELETE']:
            return True
        return False

    def has_object_permission(self, request, view, obj: Queue):
        user: UserProfile = request.user
        if obj.company.organization_id == user.organization_id:
            return True
        return False

class QueueEntryPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user: UserProfile = request.user
        queue_id = request.data.get('queue')
        if request.method in ['POST']:
            if queue := get_object_or_404(Queue, id=queue_id):
                return queue.company.organization_id == user.organization_id
        if request.method in ['PUT', 'PATCH']:
            queue = Queue.objects.filter(id=queue_id).first()
            if queue is None or queue.company.organization_id == user.organization_id:
                return True
        if request.method in ['GET', 'DELETE']:
            return True
        return False

    def has_object_permission(self, request, view, obj: QueueEntry):
        user: UserProfile = request.user
        if obj.queue.company.organization_id == user.organization_id:
            return True
        return False
