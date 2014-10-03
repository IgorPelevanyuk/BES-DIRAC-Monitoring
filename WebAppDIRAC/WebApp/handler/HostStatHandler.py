from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB

import math

def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp

class HostStatHandler(WebHandler):

    AUTH_PROPS = "all"

    def web_createDBinstance(self):
            print "Create Instance"
            self.DB = SAMDB()
            print 'DB connected'

    def web_getData(self):
            self.DB = SAMDB()
            states = self.DB.getHostStat()['Value']
            print 'INFO ', len(states), ' states had been retrieved'
            result=[]
            for st in states:
              temp = {}
              temp['site'] = st[0]
              temp['host'] = st[1]
              temp['successes24'] = st[2] if st[2]!=0 else None
              temp['total24'] = st[3] if st[3]!=0 else None
              temp['fails24'] = int(st[3]) - int(st[2])
              temp['rate24'] = trunc(int(st[2])*1.0/int(st[3])) if int(st[3])!=0 else 0

              temp['successes48'] = st[4]
              temp['total48'] = st[5]
              temp['fails48'] = int(st[5]) - int(st[4])
              temp['rate48'] = trunc(int(st[4])*1.0/int(st[5])) if int(st[5])!=0 else 0

              temp['successes'] = st[6]
              temp['total'] = st[7]
              temp['fails'] = int(st[7]) - int(st[6])
              temp['rate'] = trunc(int(st[6])*1.0/int(st[7])) if int(st[7])!=0 else 0
              result.append(temp)
            self.write({"result":result})

