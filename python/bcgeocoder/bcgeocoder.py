'''
Created on Jun 24, 2014

@author: kjnether
'''
import json
import os
import pprint
import time
import urllib2

class bcgeocoder(object):
    '''
    This is a very simple python api that wraps the 
    British Columbia geocoding web service.  
        
    :ivar addressString: The portion of the url that contains
                         the address String input.
    :ivar curDistance: The distance from the curb for the address
                       coordinates.  Default value is 0
    :ivar geoCoderURL: The Base url to the geocoding web service
    :ivar interpolation: Type of interpolation to use when geocoding
                         an address.  The default is None.
    :ivar maxAttempts: Sometimes the web service is temporarily unavailable
                       or the request times out.  This paramater determines 
                       how many attempts at querying the web service will 
                       be made.
    :ivar projParam: The type of projection for the return coordinates.
                     default is bc albers.
    :ivar waitTime: If an attempt to communicate with the web service returns
                    a 500 code. This parameter determines how long it will
                    wait until it tries again.  The unit of measurement
                    is in milliseconds.
    '''
    
    def __init__(self):
        # Not going to provide any options in terms of how the data
        # is retured.  Will always come back as geoJSON. The python code
        # will address the specifics of output formats and how to 
        # write to those.
        self.geoCoderURL = 'http://apps.gov.bc.ca/pub/geocoder/addresses.geojson'
        self.setAlbersProjection()
        self.setCurbDistance()
        self.setInterpolation()
        self.maxAttempts = 3 # the maximum number of attempts to get an address if a 500 code is received.
        self.waitTime = 3 # time in milliseconds to wait before another attempt at geocoding an address if 500 return code was received
        
    def setAlbersProjection(self):
        '''
        sets the return projection to BC albers. EPSG code 3005
        '''
        self.projParam = 'outputSRS=3005'
        
    def setGeographicProjection(self):
        '''
        Sets the return projection to geographic.
        '''
        self.projParam = 'outputSRS=4326'
        
    def setCurbDistance(self, curDistance=0):
        '''
        Used to set the curb distance parameter used in geocoding 
        an address.  Default value is 0.
        
        :param  curDistance: Integer representing the distance from 
                             the curb for the returned coordinates.
        :type curDistance: int
        '''
        # TODO: should put a check to ensrue that the arguement sent is a number
        self.curDistance = 'setBack=' + str(curDistance)
        
    def setAddressString(self, inString):
        '''
        Used to set the address string for the geocoding request.  This is 
        a place were the scripts api could be augmented.  If the address that
        we are provided has been broken up into street number, street name, 
        postal code etc.  The web service makes allowances for this type of 
        query but this python interface currently does not.
        
        :param  inString: input address string that we wish to geocode..
        :type inString: string
        '''
        # TODO: the query string is very simple at the moment Need to add some logic to check for illegal characters put in exceptions etc..
        self.addressString = 'addressString=' + inString.replace(' ', '+')
        
    def setInterpolation(self, interpType='adaptive'):
        '''
        This is the type of interpolation that is to be used when geocoding
        the address.
        
        :param  interpType: interpolation type.  Valid values include:
                            adaptive|linear|none
        :type interpType: string
        '''
        # TODO: add check to make sure the interpType is adaptive, linear, none
        self.interpolation= 'interpolation=' + interpType
        
    def geocode(self, attempt=0):
        '''
        Will geocode the address that is currently been set inside this
        object.
        
        :param  attempt: Used by this method if the attempt to communicate
                         with the geocoding service receives a 500 code.
                         When it tries again the method will automatically 
                         populate this parameter.
        :type attempt: int
        
        :returns: a Geocode object
        :rtype: bcgeocoder.bcgeocoder.Geocode object
        '''
        queries = '&'.join([self.projParam, self.curDistance, self.interpolation, self.addressString])
        queryUrl = self.geoCoderURL + '?' + queries
        
        result = urllib2.urlopen(queryUrl)
        resCode = result.getcode()
        
        geoCodedResult = None
        if resCode == 200:
            # proceed 

            # Now stuff the results into a GeoCode
            # object, and return it.
            resStr = result.read()
            geoCodedResult = Geocode(resStr)
        elif resCode == 500:
            # wait and retry
            if attempt >= self.maxAttempts:
                msg = 'Unable to retrieve an address for the string (' + \
                      self.addressString + ') Received response code ' + \
                      '500 ' + str(self.maxAttempts) + ' times.'
                raise urllib2.URLError, msg
            else:
                attempt += 1
                time.sleep(self.waitTime)
                geoCodedResult = self.geocode(attempt)
        else:
            msg = 'Received a result code of: ' + str(resCode) + ' The url ' + \
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
#             self.data = json.loads(urlResult, 'utf-8')
        
    def getCoordinates(self):
        '''
        extracts the coordinates from the returned json.
        
        :returns: a list of coordinates
        :rtype: list( x y coordinates)
        '''
        coords = None
        for feat in self.data['features']:
            if feat.has_key('geometry'):
                coords = feat['geometry']['coordinates']
        return coords
    
    def getprecisionPoints(self):
        '''
        extracts the precision point for the geocoded address 
        and returns them.
        :returns: precision points
        :rtype: int
                
        '''
        return self.data['features'][0]['properties']['precisionPoints']
        
    def pprint(self):
        ''' uses the pretty print method to print the
        data contained in this object in a nicely formatted
        manner that should make it easy to read.
        
        Used primarily for debugging
        '''
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.data)
        