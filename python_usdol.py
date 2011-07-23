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

    def _get_request(self, fmt='json', meta_only=False):
        header = self._get_header(fmt=fmt)
        qs = self.baseurl
        if meta_only:
            qs = self.metaurl
        url = urlparse.urljoin(USDOL_URL, qs)
        req = urllib2.Request(url, headers={"Authorization": header,
                                            "Accept": 'application/%s' % fmt})
        return req

    def fetch_data(self, dataset, table, fmt='json'):
        '''
        fetch_data(dataset, table[, fmt]) -> Return an object representing
        the information in the specified table from the specified dataset.
        
        'fmt' is json by default. Valid choices are 'xml' and 'json'.
        '''
        enc_opts = ['json', 'xml']
        urlstr = self._get_request(fmt)
        data = urllib2.urlopen(urlstr)
        if fmt == 'json':
            ret = json.loads(data.read())
        elif fmt not in enc_opts:
            raise AttributeError("Valid format choices are: json, xml")
        else:
            ret = data.read()
        return ret

    def fetch_metadata(self, dataset):
        '''
        fetch_metadata(dataset) -> Returns XML object containing metadata
        for the specified dataset.

        JSON encoding is unavailable for metadata.
        '''
    def get_all_agencies(self, fmt='json', meta_only=False):
        '''
        '''
        
        
                        
        
        
        
    
        
        
        
        
    
