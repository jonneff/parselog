import unittest
from cc-svds import ParseLog

class TestParseLog(unittest.TestCase): 	
    # CONSIDER ADDING PYTEST FIXTURES FOR CONSTANTS 
    def setUp( self): 
        parse = ParseLog() 
        goodlog = open('test_good.log','r')
        badlog = open('test_bad.log', 'r')

    def test_parse_apache_time_returns_correct_result(self):
        datetime = parse.parse_apache_time("30/Aug/2015:05:13:53 +0200")
        exp_datetime = 1440904433
        self.assertEqual(exp_datetime, datetime)

    def test_ip_lookup_method_returns_correct_result(self):
        org, isp, lat, lon = self.parse.ip_lookup('74.125.225.229')
        exp_org = exp_isp = 'Google Inc.'
        exp_lat = 37.419200000000004
        exp_lon = -122.0574
        self.assertEqual(exp_org, org)
        self.assertEqual(exp_isp, isp)
        self.assertEqual(exp_lat, lat)
        self.assertEqual(exp_lon, lon)

    def test_ip_lookup_method_handles_bad_ip(self):
        org, isp, lat, lon = self.parse.ip_lookup('0.0.0.0')
        exp_org = exp_isp = exp_lat = exp_lon = None
        self.assertEqual(exp_org, org)
        self.assertEqual(exp_isp, isp)
        self.assertEqual(exp_lat, lat)
        self.assertEqual(exp_lon, lon)

    def test_parse_line_method_handles_malformed_line(self):
        line = badlog.readline()
        result = self.parse.parse_line(line)
        actualLine = result[0]
        flag = result[1]
        self.assertEqual(line, actualLine)
        self.assertEqual(0, flag)

    def test_parse_line_method_returns_correct_result(self):
        line = goodlog.readline()
        result = self.parse.parse_line(line) 
        actual = result[0]
        flag = result[1]
        expected = {   
            'datetime': 1389721010,  
            'uri': '/svds.com',
            'referer': 'http://www.svds.com/rockandroll/',
            'ip': '198.0.200.105',
            'org': 'SILICON VALLEY DATA SCIENC',
            'lat': 37.8858,
            'lon': -122.118,
            'isp': 'Comcast Business Communications, LLC'
        }  
        self.assertDictEqual(expected, actual)
        self.assertEqual(1, flag)

    def __del__(self):
        # close files in destructor method
        # destructors are controversial in Python but while seems awkward in this case
        # IMPORTANT:  avoid circular references with other classes when using destructor.
        self.goodlog.close()
        self.badlog.close()

if __name__ == '__main__': unittest.main()

