from django.test import TestCase
import os, sys

sys.path.append(os.path.abspath('.'))

import pytest
import urllib


from ..weatherAU import uv_index

class TestUVIndex(TestCase):  
    def setUp(self):
        self.uv_data = uv_index.UvIndex('Vic')

    def test_invalid_state(self):
        with pytest.raises(KeyError, match='zzz'):
            uv_data = uv_index.UvIndex('zzz')


    def test_obs(self):
        assert self.uv_data is not None

    def test_acknowedgment_url(self):
        assert len(self.uv_data.url) > 0
        assert len(self.uv_data.acknowedgment) > 0

    def test_identifier(self):
        assert self.uv_data.identifier == 'IDZ00112'

    def test_aac_list(self):
        aac_list = self.uv_data.aac_list()
        assert len(aac_list) > 10

        for description in aac_list:
            assert description is not None
            assert aac_list[description] is not None

    def test_get_aac(self):
        assert self.uv_data.get_aac('Melbourne') == 'VIC_PT042'

    def test_uv(self):
        uv_message = self.uv_data.uv_message('VIC_PT042')
        assert uv_message is not None
        
        # http://reg.bom.gov.au/uv/data.shtml
        assert 'Sun protection' in uv_message
