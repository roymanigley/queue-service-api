from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework import status

from apps.authentication.models import UserProfile, Organization
from apps.core.models import QueueEntry, Company, Queue

USERNAME = 'me'
PASSWORD = '<PASSWORD>'

class QueueEntryTests(TestCase):

    def setUp(self):
        self.my_organization = Organization.objects.create(
            name='my_organization'
        )
        self.other_organization = Organization.objects.create(
            name='other_organization'
        )
        self.my_company = Company.objects.create(
            name='my_company',
            organization=self.my_organization,
        )
        self.other_company = Company.objects.create(
            name='other_company',
            organization=self.other_organization,
        )
        self.my_queue = Queue.objects.create(
            company=self.my_company,
        )
        self.other_queue = Queue.objects.create(
            company=self.other_company,
        )
        self.me = UserProfile.objects.create(
            username=USERNAME,
            organization=self.my_organization
        )
        self.me.set_password(PASSWORD)
        self.me.save()


    def test_create_for_other_queue__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='add_queueentry'))
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            '/api/queue-entries/',
            data={
                'queue': self.other_queue.id,
                'description': 'Lorem',
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_create_for_my_queue__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='add_queueentry'))
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            '/api/queue-entries/',
            data={
                'queue': self.my_queue.id,
                'description': 'Lorem',
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        data = response.json()
        created_record = QueueEntry.objects.get(id=data['id'])
        self.assertEqual(created_record.queue, self.my_queue)

    def test_create__with_out_permission(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            '/api/queue-entries/',
            data={
                'queue': self.my_queue.id,
                'description': 'Lorem',
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update_for_my_queue__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='change_queueentry'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = QueueEntry.objects.create(description='Alpha Corp', queue=self.my_queue)
        updated_description = 'Alpha Corp II'
        response = self.client.put(
            f'/api/queue-entries/{created_record.id}/',
            data={
                'description': updated_description,
                'queue': self.my_queue.id,
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        updated_record = QueueEntry.objects.get(id=created_record.id)
        self.assertEqual(updated_record.queue, self.my_queue)
        self.assertEqual(updated_record.description, updated_description)

    def test_update_for_my_company__with_permission_but_set_to_other_company(self):
        self.me.user_permissions.add(Permission.objects.get(codename='change_queueentry'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = QueueEntry.objects.create(description='Alpha Corp', queue=self.my_queue)
        updated_description = 'Alpha Corp II'
        response = self.client.put(
            f'/api/queue-entries/{created_record.id}/',
            data={
                'description': updated_description,
                'queue': self.other_queue.id,
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update_for_other_company__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='change_queueentry'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = QueueEntry.objects.create(description='Alpha Corp', queue=self.other_queue)
        updated_description = 'Alpha Corp II'
        response = self.client.put(
            f'/api/queue-entries/{created_record.id}/',
            data={
                'description': updated_description,
                'queue': self.my_queue.id,
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

    def test_update__with_out_permission(self):
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = QueueEntry.objects.create(description='Alpha Corp', queue=self.my_queue)
        updated_description = 'Alpha Corp II'
        response = self.client.put(
            f'/api/queue-entries/{created_record.id}/',
            data={
                'description': updated_description,
                'queue': self.my_queue.id,
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_delete_for_my_company__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='delete_queueentry'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = QueueEntry.objects.create(description='Alpha Corp', queue=self.my_queue)
        response = self.client.delete(
            f'/api/queue-entries/{created_record.id}/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        deleted_record_exists = QueueEntry.objects.filter(id=created_record.id).exists()
        self.assertFalse(deleted_record_exists)

    def test_delete_for_other_company__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='delete_queueentry'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = QueueEntry.objects.create(description='Alpha Corp', queue=self.other_queue)
        response = self.client.delete(
            f'/api/queue-entries/{created_record.id}/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        deleted_record_exists = QueueEntry.objects.filter(id=created_record.id).exists()
        self.assertTrue(deleted_record_exists)

    def test_delete__without_permission(self):
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = QueueEntry.objects.create(description='Alpha Corp', queue=self.my_queue)
        response = self.client.delete(
            f'/api/queue-entries/{created_record.id}/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        deleted_record_exists = QueueEntry.objects.filter(id=created_record.id).exists()
        self.assertTrue(deleted_record_exists)
