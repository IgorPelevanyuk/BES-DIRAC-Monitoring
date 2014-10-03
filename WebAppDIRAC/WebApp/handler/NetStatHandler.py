from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB

import math

def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp

class NetStatHandler(WebHandler):

    AUTH_PROPS = "all"

    def web_createDBinstance(self):
            print "Create Instance"
            self.DB = SAMDB()
            print 'DB connected'

    def web_getData(self):
            self.DB = SAMDB()
            states = self.DB.getNetStat()['Value']
            print states
            result=[]
            for st in states:
              temp = {}
              temp['site'] = st[0]
              temp['host'] = st[1]
              temp['cetype'] = st[2]
              temp['avgping'] = float(st[3])
              temp['passed'] = float(st[4])
              temp['description'] = st[5]
#              temp['rate'] = trunc(int(st[2])*1.0/int(st[3]))
              result.append(temp)
            self.write({"result":result})

