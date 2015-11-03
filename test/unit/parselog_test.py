#!/usr/bin/env python

import sys
import unittest
from app.parselog import ParseLog


class TestParseLog(unittest.TestCase): 	
    # CONSIDER ADDING PYTEST FIXTURES FOR CONSTANTS 
    def setUp( self): 
        self.parse = ParseLog() 
        self.goodlog = open('data/test_good.log','r')
        self.badlog = open('data/test_bad.log', 'r')

    def test_parse_apache_time_returns_correct_result(self):
        datetime = self.parse.parse_apache_time("30/Aug/2015:05:13:53 +0200")
        exp_datetime = 1440904433
        self.assertEqual(exp_datetime, datetime)

    def test_ip_lookup_method_returns_correct_result(self):
        org, lat, lon, isp = self.parse.ip_lookup('74.125.225.229')
        exp_org = exp_isp = 'Google Inc.'
        exp_lat = 37.419200000000004
        exp_lon = -122.0574
        self.assertEqual(exp_org, org)
        self.assertEqual(exp_isp, isp)
        self.assertEqual(exp_lat, lat)
        self.assertEqual(exp_lon, lon)

    def test_ip_lookup_method_handles_bad_ip(self):
        org, lat, lon, isp = self.parse.ip_lookup('0.0.0.0')
        exp_org = exp_isp = exp_lat = exp_lon = None
        self.assertEqual(exp_org, org)
        self.assertEqual(exp_isp, isp)
        self.assertEqual(exp_lat, lat)
        self.assertEqual(exp_lon, lon)

    def test_ip_lookup_method_handles_really_bad_ip(self):
        org, lat, lon, isp = self.parse.ip_lookup('46.246.49.254')
        exp_org = 'Portlane Network'
        exp_isp = 'PrivActually Ltd'
        exp_lat = exp_lon = None
        self.assertEqual(exp_org, org)
        self.assertEqual(exp_isp, isp)
        self.assertEqual(exp_lat, lat)
        self.assertEqual(exp_lon, lon)

    def test_ip_lookup_method_handles_non_ip(self):
        org, lat, lon, isp = self.parse.ip_lookup('Beetlejuice')
        exp_org = exp_isp = exp_lat = exp_lon = None
        self.assertEqual(exp_org, org)
        self.assertEqual(exp_isp, isp)
        self.assertEqual(exp_lat, lat)
        self.assertEqual(exp_lon, lon)

    def test_parse_line_method_handles_malformed_line(self):
        line = self.badlog.readline()
        result = self.parse.parse_line(line)
        self.assertIsNone(result)

    def test_parse_line_method_returns_correct_result(self):
        line = self.goodlog.readline()
        actual = self.parse.parse_line(line) 
        expected = [1389721010,'/svds.com','http://www.svds.com/rockandroll/','198.0.200.105','SILICON VALLEY DATA SCIENC', 
                    37.8858, -122.118, 'Comcast Business Communications, LLC']
        self.assertEqual(expected, actual)
        

    def __del__(self):
        # close files in destructor method
        # destructors are controversial in Python but while seems awkward in this case
        # IMPORTANT:  avoid circular references with other classes when using destructor.
        self.goodlog.close()
        self.badlog.close()

if __name__ == '__main__':
    unittest.main()

