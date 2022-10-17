from django.test import TestCase
from Accounts.models import User

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='testusername',
            password='testpassword',
            email='test@email.com'
        )

    def test_user_is_active(self):
        user1 = User.objects.get(username='testusername')
        self.assertEqual(user1.email, 'test@email.com')

    def test_user_id_exists(self):
        user1 = User.objects.get(username='testusername')
        self.assertFalse(user1.static_user_id)