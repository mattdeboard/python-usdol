import base64
import datetime
import httplib2
import lxml
import re
import urllib
import urllib2

from usdol_secret import API_AUTH_KEY, API_SHARED_SECRET

USDOL_URL = 'http://api.dol.gov/V1/FORMS/AgencyForms?'
HEADER_PREFIX = '/V1/FORMS/Agencies'
HEADER_TIMESTAMP = '&Timestamp='
HEADER_API_PREFIX = '&ApiKey='
HEADER_SIG_PREFIX = '&Signature='

class Connection(object):
    token = API_AUTH_KEY
    secret = API_SHARED_SECRET
    
    
    def __init__(self, *args, **kwargs):
        self.timestamp = datetime.datetime.now().isoformat()

    def _get_timestamp(self):
        '''
        Returns the Timestamp and ApiKey portions of the query string.
        
        There is a 15-minute window for an auth string with a valid
        timestamp to be accepted by the US DOL's servers.
        '''
        t = datetime.datetime.now().isoformat()
        return HEADER_TIMESTAMP + t.split('.')[0] + 'Z'

    def _get_signature(self):
        digest = hmac.new(API_SHARED_SECRET, msg=self._make_auth_str(),
                          digestmod=hashlib.sha1.digest())
        return HEADER_SIG_PREFIX + base64.b64encode(digest).decode()

    def _get_apikey(self):
        return HEADER_API_PREFIX + API_AUTH_KEY
        
    
        
        
        
        
    
