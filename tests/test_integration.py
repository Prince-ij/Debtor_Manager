import unittest
from app import app, db
from app.models import User

class AuthIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()
        self.create_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self):
        u = User(username='testuser', email='test@example.com')
        u.set_password('testpass')
        db.session.add(u)
        db.session.commit()

    def test_login_logout(self):
        # Login
        response = self.app.post('/login', data={
            'name': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Logout
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    def test_dashboard_access_without_login(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

