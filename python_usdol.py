import base64
import datetime
import httplib2
import lxml
import re
import urllib
import urllib2

from usdol_secret import API_AUTH_KEY, API_SHARED_SECRET

USDOL_URL = 'http://api.dol.gov/V1/FORMS/AgencyForms?'
HEADER_PREFIX = '/V1/FORMS/Agencies&Timestamp='
HEADER_API_PREFIX = '&ApiKey='

class Connection(object):
    token = API_AUTH_KEY
    secret = API_SHARED_SECRET
    
    def __init__(self, *args, **kwargs):
        self.timestamp = datetime.datetime.now().isoformat()

    def _make_auth_str(self):
        '''
        There is a 15-minute window for an auth string with a valid
        timestamp to be accepted by the US DOL's servers.
        '''
        t = datetime.datetime.now().isoformat()
        timestamp = t.split('.')[0] + 'Z'
        return HEADER_PREFIX + timestamp + HEADER_API_PREFIX + API_AUTH_KEY
        
        
        
        
        
    
