import base64
import datetime
import hashlib
import hmac
import httplib2
import lxml
import re
import sys
import urllib
import urllib2

from usdol_secret import API_AUTH_KEY, API_SHARED_SECRET

USDOL_URL = 'http://api.dol.gov'
HEADER_PREFIX = '/V1/FORMS/Agencies?$top=10'
HEADER_TIMESTAMP = 'Timestamp='
HEADER_API_PREFIX = '&ApiKey='
HEADER_SIG_PREFIX = '&Signature='

class Connection(object):
    token = API_AUTH_KEY
    secret = API_SHARED_SECRET
    
    def __init__(self, *args, **kwargs):
        hdr_value = self._get_signature()
        print >> sys.stdout, hdr_value
        self.headers = {'Authorization': urllib.urlencode(hdr_value),
                        'Accept': 'application/json'}
        self.auth_url = USDOL_URL + HEADER_PREFIX

    def get_data(self):
        http = httplib2.Http()
        url = self.auth_url
        print >> sys.stdout, url
        r, c = http.request(url, 'GET', headers=self.headers)
        return (r, c)
        
    def _get_timestamp(self):
        '''
        Returns the Timestamp and ApiKey portions of the query string.
        
        There is a 15-minute window for an auth string with a valid
        timestamp to be accepted by the US DOL's servers.
        '''
        t = datetime.datetime.now().isoformat()
        return t.split('.')[0] + 'Z'

    def _get_apikey(self):
        return API_AUTH_KEY

    def _get_signature(self):
        m = dict(Timestamp=self._get_timestamp(),
                 ApiKey=self._get_apikey())
        digest = hmac.new(self.secret,
                          msg=HEADER_PREFIX+urllib.urlencode(m),
                          digestmod=hashlib.sha1).digest()
        out = base64.b64encode(digest).decode()
        m.update(dict(Signature=out))
        return m
                        
        
        
        
    
        
        
        
        
    
