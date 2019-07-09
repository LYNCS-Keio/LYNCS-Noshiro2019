# -*- coding: utf-8 -*-
import unittest
from lib import rover_gps


class TestGPS(unittest.TestCase):
    def test_lat_long_reader_GPRMC(self):
        self.assertEqual(rover_gps.lat_long_reader('$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62'), [-37.86083333333333, 145.12266666666667])

    def test_lat_long_reader_GPGGA(self):
        self.assertEqual(rover_gps.lat_long_reader('$GPGGA,085120.307,3541.1493,N,13945.3994,E,1,08,1.0,6.9,M,35.9,M,,0000*5E'), [35.68582166666667, 139.75665666666666])

    def test_velocity_reader_GPRMC_course(self):
        self.assertEqual(rover_gps.velocity_reader('$GPRMC,085120.307,A,3541.1493,N,13945.3994,E,000.0,240.3,181211,,,A*6A'), [0.0, 240.3])
        
    def test_velocity_reader_GPRMC_speed(self):
        self.assertEqual(rover_gps.velocity_reader('$GPRMC,001225,A,2832.1834,N,08101.0536,W,12,25,251211,1.2,E,A*03'), [12, 25])


if __name__ == "__main__":
    unittest.main()