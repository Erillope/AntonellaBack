from django.test import TestCase
from core.common import ID
from core.user import Role
from datetime import date

class RoleApiTest(TestCase):
    route = '/api/role/'
    num_test = 10
    
    def test_create(self) -> None:
        for _ in range(self.num_test):
            role = Role.MATCHER.generate()
            with self.subTest(role=role):
                response = self.client.post(self.route+'?name='+role)
                data = response.json()['data']
                ID.validate(data['id'])
                self.assertEqual(data['name'], role.lower())
                self.assertEqual(data['created_date'], date.today().isoformat())
    
    def test_create_already_exists(self) -> None:
        for _ in range(self.num_test):
            role = Role.MATCHER.generate()
            with self.subTest(role=role):
                self.client.post(self.route+'?name='+role)
                response = self.client.post(self.route+'?name='+role)
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'AlreadyExistsRoleException')
    
    def test_rename(self) -> None:
        for _ in range(self.num_test):
            role = Role.MATCHER.generate()
            with self.subTest(role=role):
                self.client.post(self.route+'?name='+role)
                renamed_role = role[:len(role)//2].lower() + 'renamed'
                response = self.client.put(self.route+'?role='+role+f'&name={renamed_role}')
                data = response.json()['data']
                self.assertEqual(data['name'], renamed_role)
    
    def test_rename_already_exists(self) -> None:
        for _ in range(self.num_test):
            role = Role.MATCHER.generate()
            with self.subTest(role=role):
                self.client.post(self.route+'?name='+role)
                response = self.client.put(self.route+'?name='+role+'&role='+role)
                error = response.json()['error']
                self.assertEqual(response.status_code, 400)
                self.assertEqual(error, 'AlreadyExistsRoleException')
    
    def test_get_all(self) -> None:
        roles = [Role.MATCHER.generate() for _ in range(self.num_test)] + [Role.SUPER_ADMIN]
        for role in roles:
            self.client.post(self.route+'?name='+role)
        response = self.client.get(self.route)
        data = response.json()['data']
        self.assertEqual(len(data), len(roles))
        for i in range(len(data)):
            self.assertIn(roles[i].lower(), [role['name'] for role in data])
    
    def test_delete(self) -> None:
        roles = [Role.MATCHER.generate() for _ in range(self.num_test)]
        for role in roles:
            self.client.post(self.route+'?name='+role)
            response = self.client.delete(self.route+'?role='+role)
            data = response.json()['data']
            self.assertEqual(data['name'], role.lower())