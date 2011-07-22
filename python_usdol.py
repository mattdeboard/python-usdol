import datetime
import hashlib
import hmac
import urllib2
import urlparse

from usdol_secret import API_AUTH_KEY, API_SHARED_SECRET

USDOL_URL = 'http://api.dol.gov'


class Connection(object):
    token = API_AUTH_KEY
    secret = API_SHARED_SECRET
    
    def __init__(self, baseurl='/V1/FORMS/Agencies'):
        self.baseurl = baseurl

    def _urlencode(self, d):
        ret = ['%s=%s' % (k, v) for k, v in d.iteritems()]
        return '&'.join(ret)
        
    def _get_timestamp(self):
        '''
        Returns the Timestamp and ApiKey portions of the query string.
        
        There is a 15-minute window for an auth string with a valid
        timestamp to be accepted by the US DOL's servers.
        '''
        t = datetime.datetime.utcnow().replace(microsecond=0)
        t -= datetime.timedelta(minutes=1)
        return (t, t.isoformat()+'Z')

    def _get_message(self):
        date_time, timestamp = self._get_timestamp()
        header_dict = {"Timestamp": timestamp, "ApiKey": self.token}
        return (header_dict, '%s&%s' % (self.baseurl,
                                        self._urlencode(header_dict)))

    def _get_header(self):
        d, message = self._get_message()
        h = hmac.new(self.secret, message, hashlib.sha1)
        d['Signature'] = h.hexdigest()
        d['Accept'] = 'application/json'
        return self._urlencode(d)

    def _get_request(self):
        header = self._get_header()
        qs = self.baseurl
        url = urlparse.urljoin(USDOL_URL, qs)
        req = urllib2.Request(url, headers={"Authorization": header})
        return req

    def get_data(self):
        data = urllib2.urlopen(self._get_request())
        info = [line for line in data.readlines()]
        data.close()
        return info
                        
        
        
        
    
        
        
        
        
    
