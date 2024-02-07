from django.test import TestCase
import os, sys

sys.path.append(os.path.abspath('.'))

import pytest
import urllib


from ..weatherAU import observations

class TestObservations(TestCase):
    
    def setUp(self):
        self.obs_data = observations.Observations('Vic')
        
    def test_invalid_state(self):
        with pytest.raises(KeyError, match='zzz'):
            obs_data = observations.Observations('zzz')


    def test_obs(self):
        assert self.obs_data is not None

    def test_acknowedgment_url(self):
        assert len(self.obs_data.url) > 0
        assert len(self.obs_data.acknowedgment) > 0

    def test_identifier(self):
        assert self.obs_data.identifier == 'IDV60920'

    def test_station_list(self):
        stations = self.obs_data.stations()
        assert len(stations) > 10

        for station in stations:
            station_wmo_id = station['wmo-id']
            assert station_wmo_id is not None

            station_description = station['description']
            assert station_description is not None

            station_air_temperature = self.obs_data.air_temperature(station['wmo-id'])
        
    def test_air_temperature(self):
        air_temperature = self.obs_data.air_temperature('95936')
        assert air_temperature is not None

    def test_description(self):
        wmo_id = '95936'
        assert self.obs_data.station_attribute(wmo_id, 'description') == 'Melbourne (Olympic Park)'
