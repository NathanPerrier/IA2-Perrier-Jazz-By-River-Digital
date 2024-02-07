from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError

class BaseModelTest(TestCase):
    def test_database_is_live(self):
        db_conn = connections['default']
        try:
            db_conn.cursor()
        except OperationalError:
            self.fail('Database is not live')
            
    @classmethod
    def setUpTestData(cls):
        from .models import BaseModel
        
        cls.baseModel = BaseModel
        
        # Set up non-modified objects used by all test methods
        cls.test_model = BaseModel.objects.create(name='Test')
           
    def test_create_record(self):
        self.assertIsInstance(self.test_model, self.baseModel)
        self.assertEqual(self.test_model.name, 'Test')

    def test_retrieve_record(self):
        test_model = self.baseModel.objects.get(name='Test')
        self.assertEqual(test_model, self.test_model)

    def test_update_record(self):
        self.test_model.name = 'Updated Test'
        self.test_model.save()
        updated_test_model = self.baseModel.objects.get(id=self.test_model.id)
        self.assertEqual(updated_test_model.name, 'Updated Test')

    def test_delete_record(self):
        id = self.test_model.id
        self.test_model.delete()
        with self.assertRaises(self.baseModel.DoesNotExist):
            self.baseModel.objects.get(id=id)