import sys
import re
from ipwhois import IPWhois
from geoip import geolite2
from dateutil import parser
from datetime import datetime
from dateutil import tz
from ipwhois import IPDefinedError, ASNLookupError, ASNRegistryError, WhoisLookupError, HostLookupError, BlacklistError
import logging


logger = logging.getLogger(__name__)
handler = logging.FileHandler('data/parselog.log')
handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ParseLog(object):
    def __init__(self): 
        self.iptable = {}
        
    def parse_line(self, line): 
        """
        Parse log line to get date & time, uri, referer, ip address.
        Call self.ip_lookup() to get org, lat, lon and isp.
        Assumes each line in log file is in the Apache Combined Log format, returns None and logs warning message if 
        line is not in this format.
        Args:
            line (str): line in log file in the Apache Combined Log format
        Returns:
            tuple: either a dictionary containing the requested parts of the log and 1,
            or the original invalid log line and 0
        """
        # Use regular expression with match groups to extract data from log.
        logger.debug('Input line: %s', line)

        APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)\s*" (\d{3}) (\S+) \"(\S+)\" \"(.*)\"'
        match = re.search(APACHE_ACCESS_LOG_PATTERN, line)

        # If no match, line is not formatted correctly.  Return log line with flag = 0 (error).
        if match is None:
            logger.warn('ParseLog could not parse this line:  %s', line)
            return None

        # Parse Apache timestamp and convert to seconds since epoch.
        logger.debug('match.group(4) = date-time string %s', match.group(4))

        dt = self.parse_apache_time(match.group(4))

        # Set other return values
        uri = match.group(6)
        referer = match.group(10)
        ip = match.group(1)

        logger.debug('ip = %s', ip)

        # call ip_lookup(ip) to get org, lat, lon, and isp
        lookup = self.ip_lookup(ip)
        logger.debug('dt, uri, referer, ip = %s %s %s %s', str(dt), uri, referer, ip)
        logger.debug('lookup = %s', str(lookup))
        first = [dt, uri, referer, ip]
        logger.debug('first = %s', str(first))
        first.extend(lookup)
        logger.debug('after extend first = %s', str(first))
        return first

    def parse_apache_time(self, timestamp):
        d = parser.parse(timestamp.replace(':', ' ', 1))
        # Convert an aware datetime object to "seconds since the Epoch" (January 1, 1970).
        td = d - datetime(1970, 1, 1, tzinfo=tz.tzutc())
        return td.seconds + td.days * 86400
        
    def ip_lookup(self, ip):
        # given ip, look up org, isp, lat and lon
        # first, check if we have seen this ip before
        if ip in self.iptable:
            return self.iptable[ip]
        try:
            obj = IPWhois(ip, timeout = 10) # times out after 10 seconds  
            results = obj.lookup(get_referral=True)
            org = results['nets'][-1]['description']
            isp = results['nets'][0]['description']
        except (IPDefinedError, ASNLookupError, ASNRegistryError, WhoisLookupError, HostLookupError, BlacklistError) as e:
            # log bad ip and error
            logger.error('%s from IPWhois on IP %s, setting org & isp to None', e, ip)
            org = isp = None 
        except ValueError:
            logger.error('Set org & isp to None, ValueError from IPWhois for IP %s', ip)
            org = isp = None   

        # geolite2 returns NoneType if no match
        try:
            match = geolite2.lookup(ip)
            if match:
                if match.location:
                    if match.location[0]:
                        lat = match.location[0]
                    else:
                        lat = None
                        logger.warn('Set lat = None, geolite2 unable to find lat for IP %s', ip)
                    if match.location[1]:
                        lon = match.location[1]
                    else:
                        lon = None
                        logger.warn('Set lon = None, geolite2 unable to find lon for IP %s', ip)
                else:
                    lat = lon = None
                    logger.warn('Set lat & lon = None, geolite2 unable to find lat/lon for IP %s', ip)
            else:
                # log unable to find lat/lon for this ip
                logger.warn('Set lat & lon = None, geolite2 unable to find lat/lon for IP %s', ip)
                lat = lon = None
        except ValueError:
            # log bad ip and error
            logger.error('Set lat & lon = None, ValueError from geolite2 for IP %s', ip)
            lat = lon = None

        self.iptable[ip] = [org, lat, lon, isp]
        return self.iptable[ip]

if __name__ == '__main__':
    parse = ParseLog() 



