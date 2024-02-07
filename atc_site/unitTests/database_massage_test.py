from django.test import TestCase


class MessageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        from atc_site.backend.weather_app.chatbot.models import Message
        cls.message = Message
        # Set up non-modified objects used by all test methods
        Message.objects.create(content='Hello', role='User')

    def test_content_label(self):
        message = self.message.objects.get(id=1)
        field_label = message._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_role_label(self):
        message = self.message.objects.get(id=1)
        field_label = message._meta.get_field('role').verbose_name
        self.assertEqual(field_label, 'role')
    def test_role_field_type(self):
        message = self.message.objects.get(id=1)
        field_type = message._meta.get_field('role').get_internal_type()
        self.assertEqual(field_type, 'CharField')
        
    def test_content_field_type(self):
        message = self.message.objects.get(id=1)
        field_type = message._meta.get_field('content').get_internal_type()
        self.assertEqual(field_type, 'TextField')
        
    # def test_get_content(self):
    #     self.message.objects.create(content='Hello', role='User')
    #     message = self.message.objects.get(id=1)
    #     expected_object_name = f'{message.content}'
    #     self.assertEqual(expected_object_name, str('Hello'))
        
    # def test_get_role(self):
    #     self.message.objects.create(content='Hello', role='User')
    #     message = self.message.objects.get(id=1)
    #     expected_object_name = f'{message.role}'
    #     self.assertEqual(expected_object_name, str('User'))