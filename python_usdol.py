import datetime
import hashlib
import hmac
import json
import sys
import urllib2
import urlparse

from usdol_secret import API_AUTH_KEY, API_SHARED_SECRET

USDOL_URL = 'http://api.dol.gov'


class Connection(object):
    '''
    An instance of Connection represents a connection to the U.S. Dept.
    of Labor's developer API.

    Connection(token, secret[, dataset, table])

    'token' and 'secret' are the API token & shared secret is the API
    token generated at http://developer.dol.gov. Complete listing of
    valid datasets and tables are to be found at the same URL.

    Once you have instantiated Connection, call the get_data method,
    which will fetch the data according to parameters. For more info,
    consult get_data's docstring.
    '''
    token = API_AUTH_KEY
    secret = API_SHARED_SECRET
    
    def __init__(self, token=API_AUTH_KEY, secret=API_SHARED_SECRET,
                 dataset='FORMS', table='Agencies'):
        self.baseurl = '/V1/%s/%s' % (dataset, table)

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

    def _get_header(self, fmt='json'):
        d, message = self._get_message()
        h = hmac.new(self.secret, message, hashlib.sha1)
        d['Signature'] = h.hexdigest()
        return self._urlencode(d)

    def _get_request(self, fmt='json'):
        header = self._get_header(fmt=fmt)
        qs = self.baseurl
        url = urlparse.urljoin(USDOL_URL, qs)
        req = urllib2.Request(url, headers={"Authorization": header,
                                            "Accept": 'application/%s' % fmt})
        return req

    def get_data(self, fmt='json'):
        '''
        get_data([fmt="json"]) -> Python dictionary
        get_data([fmt="xml"]) -> XML object
        '''
        data = urllib2.urlopen(self._get_request(fmt=fmt))
        if fmt == 'json':
            ret = json.loads(data.read())
        else:
            ret = data.read()
        return ret
                        
        
        
        
    
        
        
        
        
    
