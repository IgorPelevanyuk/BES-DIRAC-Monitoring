from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB

import math

def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp
  

class TestHandler(WebHandler):

    AUTH_PROPS = "all"

    def web_createDBinstance(self):
            print "Create Instance"
            self.DB = SAMDB()
            print 'DB connected'

    def web_getData(self):
            self.DB = SAMDB()
            states = self.DB.getState()['Value']
            result=[]
            for st in states:
              temp = {}
              temp['site'] = st[0]
              temp['service'] = st[1]
              temp['test'] = st[2]
              temp['result'] = st[3]
              temp['description'] = st[4]
              temp['reliability24'] = trunc(float(st[7]))
              temp['reliability48'] = trunc(float(st[8]))
              temp['reliability168'] = trunc(float(st[9]))
              result.append(temp)
            self.write({"result":result})
	
    def web_setData(self):
            value = self.request.arguments["value"][0]
            print value
            self.DB = TestDB()
            res = self.DB.insert_val(value)
            self.write({"value": res})

