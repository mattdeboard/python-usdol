#!/usr/bin/env python
'''
Python-USDOL

Python module for access to the U.S. Department of Labor datasets via
its developer API. (http://developer.dol.gov)
'''

__version__ = "1.0"
__license__ = "BSD"
__copyright__ = "Copyright 2011, Matt DeBoard"
__author__ = "Matt DeBoard <http://mattdeboard.net>"


import datetime
import hashlib
import hmac
import json
import string
import urllib2

USDOL_URL = 'http://api.dol.gov'
API_VER = 'V1'


class Connection(object):
    """
    An instance of Connection represents a connection to the U.S. Dept.
    of Labor's developer API.

    Connection(token, secret[, dataset, table])

    'token' and 'secret' are the API token & shared secret is the API
    token generated at http://developer.dol.gov. Complete listing of
    valid datasets and tables are to be found at the same URL.

    Once you have instantiated Connection, call the get_data method,
    which will fetch the data according to parameters. For more info,
    consult get_data's docstring.
    
    """
    def __init__(self, token=None, secret=None):
        self.token = token
        self.secret = secret

    def _urlencode(self, d):
        ret = ['%s=%s' % (k, v) for k, v in d.iteritems()]
        return '&'.join(ret)
        
    def _get_timestamp(self):
        """
        Returns the Timestamp and ApiKey portions of the query string.
        
        There is a 15-minute window for an auth string with a valid
        timestamp to be accepted by the US DOL's servers.
        
        """
        t = datetime.datetime.utcnow().replace(microsecond=0)
        t -= datetime.timedelta(minutes=1)
        return (t, t.isoformat()+'Z')

    def _get_message(self, qs):
        """
        Generates the message to be hashed by HMAC SHA1 algorithm and
        passed to the API in the "Authorization" header.

        """
        baseurl = '/%s/%s/' % (API_VER, self.dataset)
        if self.table != '$metadata':
            baseurl += self.table
        baseurl += qs
        date_time, timestamp = self._get_timestamp()
        header_dict = {"Timestamp": timestamp, "ApiKey": self.token}
        return (header_dict, '%s&%s' % (baseurl, self._urlencode(header_dict)))

    def _get_header(self, qs):
        d, message = self._get_message(qs)
        h = hmac.new(self.secret, message, hashlib.sha1)
        d['Signature'] = h.hexdigest()
        return self._urlencode(d)

    def _get_querystring(self, **kwargs):
        """
        Generates the query string which will be appended to the URL of
        the target dataset/table, e.g.:

        ?&top=10&skip=20

        """
        qs = []
        for arg in kwargs:
            if kwargs[arg]:
                # `filter` is a keyword in Python, so I avoid using it by
                # adding a _ to the end, then removing it here.
                key = arg.replace('_', '')
                val = kwargs[arg].replace(' ', '+')
                qs.append("$%s=%s" % (key, val))
        return '?' + string.join(qs, '&')

    def _get_request(self, qs='', fmt='json'):
        url_args = [USDOL_URL, API_VER, self.dataset, self.table]
        header = self._get_header(qs)
        url = string.join(url_args, '/') + qs
        req = urllib2.Request(url, headers={"Authorization": header,
                                            "Accept": 'application/%s' % fmt})
        return req

    def fetch_data(self, dataset, table='$metadata', fmt='json', top=0,
                   skip=0, select='', orderby='', filter_=''):
        """
        fetch_data(dataset, table[, fmt, top, skip, select, orderby]) ->
        
            Return an object representing the information in the specified
            table from the specified dataset.

            The rest of the args work as outlines in the DOL's API
            reference (http://developer.dol.gov/html-req.htm).
        
        'fmt' is json by default. Valid choices are 'xml' and 'json'.
        
        """
        
        qs = self._get_querystring(top=top, skip=skip, select=select,
                                   orderby=orderby, filter_=filter_)
        self.dataset = dataset
        self.table = table
        enc_opts = ['json', 'xml']
        if fmt not in enc_opts:
            raise AttributeError("Valid format choices are: json, xml")
        if table == '$metadata' and fmt != 'xml':
            fmt = 'xml'
    
        urlstr = self._get_request(qs, fmt)
        data = urllib2.urlopen(urlstr)
        if fmt == 'json':
            d = json.loads(data.read())['d']
            ret = d.get('results', d)
        else:
            ret = data.read()
        return ret
