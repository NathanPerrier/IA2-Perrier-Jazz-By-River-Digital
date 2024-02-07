from django.test import TestCase
import os, sys

sys.path.append(os.path.abspath('.'))

import pytest
import urllib


from ..weatherAU import place

class TestPlace(TestCase):
    def setUp(self):
        self.place_data = place.Place('vic', 'parkville')
        self.place_data2 = place.Place('vic', 'endeavour-hills')

    def test_404(self):
        with pytest.raises(urllib.error.HTTPError, match='HTTP Error 404: Not Found'):
            place_data = place.Place('vic', 'zzz')


    def test_obs(self):
        assert self.place_data is not None

    def test_acknowedgment_url(self):
        assert len(self.place_data.url) > 0
        assert len(self.place_data.acknowedgment) > 0

    def test_station_id(self):
        station_id = self.place_data.station_id()
        assert station_id is not None
        assert len(station_id) == 5

    def test_forecast_parkville(self):
        forecast = self.place_data.forecast()
        assert 'issued' in forecast
        assert 'date' in forecast
        assert 'precis' in forecast

    def test_air_temperature(self):
        air_temperature = self.place_data.air_temperature()
        assert air_temperature is not None
        assert air_temperature > -30.0
        assert air_temperature < 60.0

    def test_forecast_endeavour_hills(self):
        forecast = self.place_data2.forecast()
        assert 'issued' in forecast
        assert 'date' in forecast
        #assert 'precis' in forecast
