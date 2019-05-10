import os
import pandas as pd

class ofsets:
    def __init__(self, case_dir, filename, time = None):
        self.filename = filename
        if time == None:
            self.time = self._getLatestTime(case_dir + "/postProcessing/sets/")
        else:
            self.time = str(time)
            
        filePath = case_dir + "/postProcessing/sets/" + self.time + "/" + filename
        self.data = pd.read_csv(filePath)
        self.fieldNames = self.data.columns
        
    def _getLatestTime(self,path):
        dirs = os.listdir(path)
        return dirs[-1]
    
    #get field in dataFrame
    def get(self, fieldName): 
        if fieldName not in self.fieldNames:
            raise ValueError( 'fieldName not in fieldNames.')
        return self.data[fieldName]