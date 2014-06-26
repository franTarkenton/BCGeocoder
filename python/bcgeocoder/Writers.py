'''
Created on Jun 26, 2014

@author: kjnether
'''
import csv
import os.path


class WriteCSV():
    
    def __init__(self, file2Write, header=None):
        self.file2Write = file2Write
        # TODO: warning if file already exists.
        self.fh = open(file2Write, 'wb')
        self.header = header
        if header:
            self.csvWriter = csv.DictWriter(self.fh, fieldnames=header)
            self.csvWriter.writeheader()
        else:
            self.csvWriter = csv.writer(self.fh)                
    
    def addRow(self, row):
        
        cnt = 0
        if self.csvWriter.__class__.__name__ == 'DictWriter':
            rowDict = {}
            for colName in self.header:
                rowDict[colName] = row[cnt]
                cnt += 1
            row = rowDict
        self.csvWriter.writerow(row)
    
    def finish(self):
        self.close()
    
    def close(self):
        self.fh.close()
    
# The following code was used in dev. should get moved to a test
# if __name__ == '__main__':
#     testFile = os.path.join(os.path.dirname(__file__), 'testfile.csv')
#     header = ['col1', 'col2']
#     data = [[1,2], [3,4], [4,5], [5,6]]
# #     csvWriter = WriteCSV(testFile, header)
#     csvWriter = WriteCSV(testFile)
#     for row in data:
#         csvWriter.addRow(row)
#     csvWriter.finish()

    
    
    