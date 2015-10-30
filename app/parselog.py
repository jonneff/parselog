import sys
import re
from ipwhois import IPWhois
from geoip import geolite2
from dateutil import parser
from datetime import datetime
from dateutil import tz

class ParseLog(object):
    # def __init__(self): 
    # any initialization
        
    def parse_line(self, line): 
        """
        Parse log line to get date & time, uri, referer, ip address.
        Call self.ip_lookup() to get org, lat, lon and isp.
        Assumes each line in log file is in the Apache Combined Log format, returns line with 
        error flag if line is not in this format.
        Args:
            line (str): line in log file in the Apache Combined Log format
        Returns:
            tuple: either a dictionary containing the requested parts of the log and 1,
            or the original invalid log line and 0
        """
        # Use regular expression with match groups to extract data from log.
        APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)\s*" (\d{3}) (\S+) ([ ^"]*) ([ ^"]*)'
        match = re.search(APACHE_ACCESS_LOG_PATTERN, line)

        # If no match, line is not formatted correctly.  Return log line with flag = 0 (error).
        if match is None:
            return (line, 0)

        # Parse Apache timestamp and convert to seconds since epoch.
        datetime = self.parse_apache_time(match.group(4))

        # Set other return values
        uri = match.group(6)
        referer = match.group(10)
        ip = match.group(1)

        # call ip_lookup(ip) to get org, lat, lon, and isp
        org, isp, lat, lon = self.ip_lookup(ip)
        result = {
            'datetime': datetime, 
            'uri': uri,
            'referer': referer,
            'ip': ip,
            'org': org,
            'lat': lat,
            'lon': lon,
            'isp': isp
        }
        return (result, 1)

    def parse_apache_time(self, timestamp):
        d = parser.parse(timestamp.replace(':', ' ', 1))
        # Convert an aware datetime object to "seconds since the Epoch" (January 1, 1970).
        td = d - datetime(1970, 1, 1, tzinfo=tz.tzutc())
        return td.seconds + td.days * 86400
        
    def ip_lookup(self, ip):
        # given ip, look up org, isp, lat and lon
        # need some try-catch blocks here for exception handling
        # for IPWhois need to catch IPDefinedError
        obj = IPWhois(ip)
        results = obj.lookup(get_referral=True)
        org = results['nets'][-1]['description']
        isp = results['nets'][0]['description']
        # geolite2 returns NoneType if no match
        match = geolite2.lookup(ip)
        lat = match[0]
        lon = match[1]
        return org, isp, lat, lon   

# if __name__ == '__main__': 
#     parse = ParseLog() 
#     line = parse.parse_line(line)
#     while line:
#         print line


