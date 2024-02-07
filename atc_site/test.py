import os
import sys
from django.test import TestCase
import pytest
import os
import sys
from unittest.mock import patch, Mock
from django.test import TestCase
from manage import main
from django.test.utils import setup_test_environment, teardown_test_environment

from .unitTests.__init__ import TestAllModels

class TestManageCommands(TestCase):
    '''
    Tests the manage.py file. and init teests for the rest of the app.
    '''
    
    TestAllModels()  
    
    # def setUp(self):
    #     try: setup_test_environment()
    #     except: pass

    # def tearDown(self):
    #     try: teardown_test_environment()
    #     except: pass


    # Sets the DJANGO_SETTINGS_MODULE environment variable to "atc_site.settings".
    def test_main_runs_execute_from_command_line(self):
        with patch.object(sys, 'argv', ['manage.py', 'runserver']):
            with patch('django.core.management.execute_from_command_line') as mock_execute:
                main()
                mock_execute.assert_called_once_with(sys.argv)

    def test_main_raises_import_error(self):
        with patch('django.core.management.execute_from_command_line', side_effect=ImportError):
            with self.assertRaises(ImportError):
                main()
        