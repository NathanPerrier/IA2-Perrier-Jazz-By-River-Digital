from django.test import TestCase

class AuthDbModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        from ..models import CustomUser 
        from ..models import CustomUserManager 
        
        cls.customUserManager = CustomUserManager()
        cls.customUser = CustomUser
        
        # Set up non-modified objects used by all test methods
        cls.user = CustomUser.objects.create_user(
            email='test@example.com', 
            password='testpassword', 
            first_name='Test', 
            last_name='User'
        )

    def test_create_user(self):
        self.assertIsInstance(self.user, self.customUser)
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_normalize_email(self):
        email = 'Test@Example.COM'
        normalized_email = self.customUserManager.normalize_email(email)
        self.assertEqual(normalized_email, 'test@example.com')

    def test_get_by_email(self):
        user = self.customUser.objects.get_by_email('test@example.com')
        self.assertEqual(user, self.user)

    def test_get_by_id(self):
        user = self.customUser.objects.get_by_id(self.user.id)
        self.assertEqual(user, self.user)

    def test_authenticate(self):
        user = self.customUser.objects.authenticate('test@example.com', 'testpassword')
        self.assertEqual(user, self.user)
    def test_retrieve(self):
        base_model = self.customUser.objects.get(first_name='Test')
        self.assertEqual(base_model, self.user)

    def test_update(self):
        self.user.first_name = 'Updated Test'
        self.user.save()
        updated_base_model = self.customUser.objects.get(id=self.user.id)
        self.assertEqual(updated_base_model.first_name, 'Updated Test')

    def test_delete(self):
        id = self.user.id
        self.user.delete()
        with self.assertRaises(self.customUser.DoesNotExist):
            self.customUser.objects.get(id=id)