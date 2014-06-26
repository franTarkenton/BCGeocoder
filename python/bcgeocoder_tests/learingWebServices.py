'''
Created on Jun 24, 2014

@author: kjnether
'''
import unittest
import urllib2
import json
import pprint



class LearningWebServices(unittest.TestCase):


    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def BatchGeoCoder_test(self):
        srcFile = ''
        pass 

    def WebServiceConnectSingleAddressLookup_test(self):
        print 'hello'
        streetAddress = '144 Fraser Street Lytton BC'
        
        streetAddress = streetAddress.replace(' ', '%')
        
        query = 'addressString=' + streetAddress
        # projection options 3005 albers - others also available, could supply 
        # any projection using pyproj or ogr
        query = 'interpolation=none' + '&' + 'outputSRS=3005' + '&' + query
        url = 'http://apps.gov.bc.ca/pub/geocoder/addresses.geojson' + '?' + query
        print 'url:'
        print url
        result = urllib2.urlopen(url)
        print 'returned value:'
        print 'result code:', result.getcode()
        print 'rescode type:', type(result.getcode())
        resultJSONstr = result.read()
        resultObj = json.loads(resultJSONstr)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(resultObj)
        print '..done!'
        
        # get just the coords
        for feat in resultObj['features']:
            if feat.has_key('geometry'):
                coords = feat['geometry']['coordinates']
                print 'coords:', coords
                print 'EPSG:', feat['geometry']['crs']['properties']['code']
        
        # could be re-projected with pyproj or ogr
        


    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    suite = unittest.TestSuite()
#     suite.addTest(LicenseParserTest('test_readLicensData'))
#     suite.addTest(LicenseParserTest('test_getProduct'))
    suite.addTest(LearningWebServices('WebServiceConnectSingleAddressLookup_test'))
    unittest.TextTestRunner().run(suite)
#     unittest.main()


