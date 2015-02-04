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


