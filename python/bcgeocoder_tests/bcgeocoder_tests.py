'''
Created on Jun 25, 2014

@author: kjnether
'''
import unittest
import bcgeocoder.bcgeocoder as bcgeocoder


class GeocoderTests(unittest.TestCase):


    def setUp(self):
        self.geocodeObj = bcgeocoder.bcgeocoder()
        self.addressString = '144 Fraser Street Lytton BC'

        self.geocodeObj.setAddressString(self.addressString)

    def tearDown(self):
        pass

    def test_GeoCode(self):
        ''' set up is going to try to retrieve an 
        address that we know information about.  Then 
        This test will assert that all the information 
        that is being returned is correct
        '''
        geocodeObj = self.geocodeObj.geocode()
        geocodeObj.pprint()
        print 'coords are:', geocodeObj.getCoordinates()
        print 'getprecisionPoints are:', geocodeObj.getprecisionPoints()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    suite = unittest.TestSuite()
    suite.addTest(GeocoderTests('test_GeoCode'))
    unittest.TextTestRunner().run(suite)
#     unittest.main()


