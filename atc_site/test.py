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

    # Sets the DJANGO_SETTINGS_MODULE environment variable to "atc_site.settings".
    def test_main_runs_execute_from_command_line(self):
        """
        Test if the main function runs execute_from_command_line with the correct arguments.

        This test case uses patch.object to mock the sys.argv list to ['manage.py', 'runserver'].
        It also uses patch to mock the django.core.management.execute_from_command_line function.
        The main function is then called, and the mock_execute.assert_called_once_with method is used to assert that execute_from_command_line was called with the correct arguments.

        This test ensures that the main function correctly executes the Django management command 'runserver' when called.

        """
        with patch.object(sys, 'argv', ['manage.py', 'runserver']):
            with patch('django.core.management.execute_from_command_line') as mock_execute:
                main()
                mock_execute.assert_called_once_with(sys.argv)

    def test_main_raises_import_error(self):
        """
        Test the main function to ensure it raises an ImportError when execute_from_command_line raises an ImportError.
        """
        with patch('django.core.management.execute_from_command_line', side_effect=ImportError):
            with self.assertRaises(ImportError):
                main()
        