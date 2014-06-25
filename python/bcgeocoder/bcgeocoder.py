'''
Created on Jun 24, 2014

@author: kjnether
'''
import json
import pprint
import time
import urllib2


class bcgeocoder(object):
    
    def __init__(self):
        # Not going to provide any options in terms of how the data
        # is retured.  Will always come back as geoJSON. The python code
        # will address the specifics of output formats and how to 
        # write to those.
        self.geoCoderURL = 'http://apps.gov.bc.ca/pub/geocoder/addresses.geojson'
        self.setAlbersProjection()
        self.setCurbDistance()
        self.maxAttempts = 3 # the maximum number of attempts to get an address if a 500 code is received.
        self.waitTime = 3 # time in milliseconds to wait before another attempt at geocoding an address if 500 return code was received
        
    def setAlbersProjection(self):
        self.projParam = 'outputSRS=3005'
        
    def setGeographicProjection(self):
        self.projParam = 'outputSRS=4326'
        
    def setCurbDistance(self, curDistance=0):
        # TODO: should put a check to ensrue that the arguement sent is a number
        self.curDistance = 'setBack=' + str(curDistance)
        
    def setAddressString(self, inString):
        # TODO: the query string is very simple at the moment Need to add some logic to check for illegal characters put in exceptions etc..
        self.addressString = inString.replace(' ', '%')
        
    def setInterpolation(self, interpType='none'):
        # TODO: add check to make sure the interpType is adaptive, linear, none
        self.interpolation= 'interpolation=' + interpType
        
    def geocode(self, attempt=0):
        queries = '&'.join([self.projParam, self.curDistance, self.interpolation, self.addressString])
        queryUrl = self.geoCoderURL + '?' + queries
        result = urllib2.urlopen(queryUrl)
        resCode = result.getcode()
        geoCodedResult = None
        if resCode == 200:
            # proceed
            # Now stuff the results into a GeoCode
            # object, and return it.
            geoCodedResult = Geocode(result.read())
        elif resCode == 500:
            # wait and retry
            if attempt >= self.maxAttempts:
                msg = 'Unable to retrieve an address for the string (' + \
                      self.addressString + ') Received response code ' + \
                      '500 three times.'
                raise urllib2.URLError, msg
            else:
                attempt += 1
                time.sleep(self.waitTime)
                geoCodedResult = self.geocode(attempt)
        else:
            msg = 'Recieved a result code of: ' + str(resCode) + ' The url ' + \
                 'that we were requesting is: (' + str(queryUrl) + ') unable to ' + \
                 'get the results we are looking for from that url.'
            raise urllib2.URLError, msg
        return  geoCodedResult
        
class Geocode(object):
    '''
    A class that wraps the geocoder result data, and 
    adds some simple methods that make it easy to pull
    the information out of the returned json data.
    '''
    
    def __init__(self, urlResult):
        self.data = json.loads(urlResult)
        
    def getCoordinates(self):
        coords = None
        for feat in self.data['features']:
            if feat.has_key('geometry'):
                coords = feat['geometry']['coordinates']
        return coords
    
    def getprecisionPoints(self):
         return self.data['features'][0]['properties']['precisionPoints']
        
    def pprint(self):
        ''' uses the pretty print method to print the
        data contained in this object in a nicely formatted
        manner that should make it easy to read.
        
        Used primarily for debugging
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.data)
        
        
        
if __name__ == '__main__':
    