'''
Created on Jun 25, 2014

@author: kjnether
'''


import bcgeocoder.bcgeocoder as bcgeocoder
import bcgeocoder.Readers as Reader
import bcgeocoder.Writers as Writer
import sys
import os.path


class RunGeoCoderOnFile():
    
    def __init__(self):
        self.usage = os.path.basename(__file__) + ' <csv file to geocode>, <column name with address string> <output file with address Info>'
        self.checkAndGetArgs()
        self.geocodeObj = bcgeocoder.bcgeocoder()
        
    def checkAndGetArgs(self):
        if len(sys.argv) < 4:
            raise TypeError, 'Must supply the name of the csv file to read and the ! ' + self.usage
        self.addressColumn = sys.argv[2]
        self.addressInFile = sys.argv[1]
        self.outFile = sys.argv[3]
        
    def runGeoCoder(self):
        reader = Reader.ReadCSV(self.addressInFile)
        header = reader.getHeader()
        header.extend(['x', 'y', 'precision'])
        writer = Writer.WriteCSV(self.outFile, header)
        
        for row in reader:
            address = reader.getcell(row, self.addressColumn)
            print 'address:', address
            self.geocodeObj.setAddressString(address)
            geoCodeResults = self.geocodeObj.geocode()
            coordList = geoCodeResults.getCoordinates()
            precisionPoints = geoCodeResults.getprecisionPoints()
            row.extend([coordList[0], coordList[1], precisionPoints])
            writer.addRow(row)
        writer.finish()
        
if __name__ == '__main__':
    obj = RunGeoCoderOnFile()
    obj.runGeoCoder()
    
# W:\ilmb\vic\geobc\bier\p15\P15_0096_geocoder\python\bcgeocoder_tests\testData.csv address W:\ilmb\vic\geobc\bier\p15\P15_0096_geocoder\python\bcgeocoder_tests\testDataCODED.csv
            
            
            