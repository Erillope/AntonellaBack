from django.test import TestCase
from core.common import ID
from datetime import date
from .test_data import DataFactory

class RoleApiTest(TestCase):
    route = '/api/role/'
    
    def test_create(self) -> None:
        for role in DataFactory.user_test_data.get_roles():
            with self.subTest(role=role):
                response = self.client.post(self.route+'?name='+role)
                data = response.json()['data']
                ID.validate(data['id'])
                self.assertEqual(data['name'], role.lower())
                self.assertEqual(data['created_date'], date.today().isoformat())
    
    def test_create_already_exists(self) -> None:
        for role in DataFactory.user_test_data.get_roles():
            with self.subTest(role=role):
                self.client.post(self.route+'?name='+role)
                response = self.client.post(self.route+'?name='+role)
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'AlreadyExistsRoleException')
    
    def test_rename(self) -> None:
        for role in DataFactory.user_test_data.get_roles():
            with self.subTest(role=role):
                self.client.post(self.route+'?name='+role)
                response = self.client.put(self.route+'?role='+role+f'&name={role}renamed')
                data = response.json()['data']
                self.assertEqual(data['name'], role.lower()+'renamed')
    
    def test_rename_already_exists(self) -> None:
        for role in DataFactory.user_test_data.get_roles():
            with self.subTest(role=role):
                self.client.post(self.route+'?name='+role)
                response = self.client.put(self.route+'?name='+role+'&role='+role)
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'AlreadyExistsRoleException')
    
    def test_get_all(self) -> None:
        roles = DataFactory.user_test_data.get_roles()
        for role in roles:
            self.client.post(self.route+'?name='+role)
        response = self.client.get(self.route)
        data = response.json()['data']
        self.assertEqual(len(data), len(roles))
        for i in range(len(data)):
            self.assertEqual(data[i]['name'], roles[i].lower())
    
    def test_delete(self) -> None:
        roles = DataFactory.user_test_data.get_roles()
        for role in roles:
            self.client.post(self.route+'?name='+role)
            response = self.client.delete(self.route+'?role='+role)
            data = response.json()['data']
            self.assertEqual(data['name'], role.lower())