from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB

import math

def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp


class SAMCEChartsHandler(WebHandler):

    AUTH_PROPS = "all"

    def web_createDBinstance(self):
            print "Create Instance"
            self.DB = SAMDB()
            print 'DB connected'

    def web_getData(self):
            result = [{'time':0, 'state':1}, {'time':1, 'state':0}]
            self.write({"result":result})

    def web_getSiteChartData(self):
            self.DB = SAMDB()
            site = self.request.arguments['site'][0]
            states = self.DB.getSiteHistory(site)['Value']
            result=[]
            for st in states:
              temp = {}
              temp['time'] = st[0].strftime('%s')
              temp['state'] = 1 if st[1]=='Success' else 0
              result.append(temp)
            self.write({"result":result})
    
    def web_getSiteMonthAvailability(self):
            self.DB = SAMDB()
            site = self.request.arguments['site'][0]
            availability = self.DB.getSiteMonthAvailability(site)['Value']
            print availability
            result=[]
            for st in availability:
              temp = {}
              temp['time'] = int(st[1])
              temp['state'] = trunc(float(st[2]))
              result.append(temp)
            print result
            self.write({"result":result})

    def web_setData(self):
            value = self.request.arguments["value"][0]
            print value
            self.DB = TestDB()
            res = self.DB.insert_val(value)
            self.write({"value": res})

