'''
Created on Jun 25, 2014

@author: kjnether
'''
import site
import os.path
depsDir = os.path.join(os.path.dirname(__file__), '..', 'deps\Lib\site-packages')
#depsDir = r'W:\ilmb\vic\geobc\bier\p15\P15_0096_geocoder\python\deps\Lib\site-packages'
site.addsitedir(depsDir) # @UndefinedVariable
import xlrd # @UnresolvedImport
import csv

class ReadCSV():
    
    def __init__(self, inputCSVFile):
        self.inputCSVFile = inputCSVFile
        inputCSVFH = open(self.inputCSVFile, 'rU')
        self.reader = csv.reader(inputCSVFH)
        self.header = self.reader.next()
        print 'header is', self.header
        
    def getHeader(self):
        return self.header
        
    def __iter__(self):
        return self
        
    def next(self):
        return self.reader.next()
    
    def getcell(self, row, headerValue):
        cnt = 0
        headerValue = headerValue.strip()
        for i in self.header:
            i = i.strip()
            if i == headerValue:
                return row[cnt]
            else:
                cnt +=1
        return None
        
        
    


# used for testing
if __name__ == '__main__':
    print 'here'
    csvFile = r'W:\ilmb\vic\geobc\bier\p15\P15_0096_geocoder\python\bcgeocoder_tests\testData.csv'
    obj = ReadCSV(csvFile)
    for i in obj:
        print i
    
#     line = obj.next()
#     print line






