import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Rodrigo",
            "last_name": "Ferrer",
            "email": "ferrer@gmail.com",
        })
        self.assertEqual(response.status_code, 201)
    
   
    def test_create_user_duplicated_email(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "Rodrigo",
            "last_name": "Rodriguez",
            "email": "bruno@example.com",
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bruno",
            "last_name": "Dos Santos",
            "email": "bruno@example.com",  
        })
        self.assertEqual(response.status_code, 400)


    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    
    def test_get_user_by_id(self):

        res = self.client.post('/api/v1/users/', json={
            "first_name": "Jhon",
            "last_name": "Doe",
            "email": "jhon.doe@example.com",
        })        
        user = res.get_json()  
        self.assertIn('id', user)
        user_id = user['id']
    
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)


    def test_get_user_by_id_not_found(self):
        response = self.client.get('/api/v1/users/166')
        self.assertEqual(response.status_code, 404)

    def test_create_place(self):

        usuario = self.client.post('/api/v1/users/', json={
            "first_name": "Jhon",
            "last_name": "Doe",
            "email": "jhon.doe@example.com"
        })

        owner = usuario.json
        self.assertIn('id', owner)
        owner_id = owner['id']

        response = self.client.post('/api/v1/places/', json={
                "title": "Nice place",
                "description": "Good place to stay",
                "price": 100.0,
                "latitude": 37.7749,
                "longitude": -122.4194,
                "owner_id": f"{owner_id}"
        })
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()