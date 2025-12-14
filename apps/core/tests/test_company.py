from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework import status

from apps.authentication.models import UserProfile, Organization
from apps.core.models import Company

USERNAME = 'me'
PASSWORD = '<PASSWORD>'

class CompanyTests(TestCase):

    def setUp(self):
        self.my_organization = Organization.objects.create(
            name='my_organization'
        )
        self.other_organization = Organization.objects.create(
            name='other_organization'
        )
        self.me = UserProfile.objects.create(
            username=USERNAME,
            organization=self.my_organization
        )
        self.me.set_password(PASSWORD)
        self.me.save()

    def test_create__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='add_company'))
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            '/api/companies/',
            data={
                'name': 'Alpha Corp'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        data = response.json()
        created_record = Company.objects.get(id=data['id'])
        self.assertEqual(created_record.organization, self.my_organization)

    def test_create__with_out_permission(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(
            '/api/companies/',
            data={
                'name': 'Alpha Corp'
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='change_company'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = Company.objects.create(name='Alpha Corp', organization=self.my_organization)
        updated_name = 'Alpha Corp II'
        response = self.client.put(
            f'/api/companies/{created_record.id}/',
            data={
                'name': updated_name
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        data = response.json()
        updated_record = Company.objects.get(id=created_record.id)
        self.assertEqual(updated_record.organization, self.my_organization)
        self.assertEqual(updated_record.name, updated_name)

    def test_update__other_organization(self):
        self.me.user_permissions.add(Permission.objects.get(codename='change_company'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = Company.objects.create(name='Alpha Corp', organization=self.other_organization)
        updated_name = 'Alpha Corp II'
        response = self.client.put(
            f'/api/companies/{created_record.id}/',
            data={
                'name': updated_name
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)

    def test_update__without_permission(self):
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = Company.objects.create(name='Alpha Corp', organization=self.my_organization)
        updated_name = 'Alpha Corp II'
        response = self.client.put(
            f'/api/companies/{created_record.id}/',
            data={
                'name': updated_name
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_delete__with_permission(self):
        self.me.user_permissions.add(Permission.objects.get(codename='delete_company'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = Company.objects.create(name='Alpha Corp', organization=self.my_organization)
        updated_name = 'Alpha Corp II'
        response = self.client.delete(
            f'/api/companies/{created_record.id}/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        deleted_record_exists = Company.objects.filter(id=created_record.id).exists()
        self.assertFalse(deleted_record_exists)

    def test_delete__other_organization(self):
        self.me.user_permissions.add(Permission.objects.get(codename='delete_company'))
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = Company.objects.create(name='Alpha Corp', organization=self.other_organization)
        updated_name = 'Alpha Corp II'
        response = self.client.delete(
            f'/api/companies/{created_record.id}/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.content)
        deleted_record_exists = Company.objects.filter(id=created_record.id).exists()
        self.assertTrue(deleted_record_exists)

    def test_delete__without_permission(self):
        self.client.login(username=USERNAME, password=PASSWORD)

        created_record = Company.objects.create(name='Alpha Corp', organization=self.my_organization)
        updated_name = 'Alpha Corp II'
        response = self.client.delete(
            f'/api/companies/{created_record.id}/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        deleted_record_exists = Company.objects.filter(id=created_record.id).exists()
        self.assertTrue(deleted_record_exists)
