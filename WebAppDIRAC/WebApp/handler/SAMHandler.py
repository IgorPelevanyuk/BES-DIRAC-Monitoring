from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB

import math

STATE_MAP = {'Success':5,
             'Timeout':4,
             'Banned':1,
             'Fail':2,}

def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp
  
def getStateNumber(state):
    if state in STATE_MAP:
        return STATE_MAP[state]
    return 2

class SAMHandler(WebHandler):

    AUTH_PROPS = "all"

    def web_getData(self):
            self.DB = SAMDB()
            states = self.DB.getState()['Value']
            result=[]
            for st in states:
              temp = {}
              temp['site'] = st[0]
              temp['test'] = st[1]
              temp['result'] = st[2]
              temp['received'] = st[3]
              temp['description'] = st[4]
              result.append(temp)
            self.write({"result":result})

    def selectFromDB(self, site, test):
        selectSQL = "SELECT R.last_update, R.state, R.description FROM Results R, Sites S, Tests T WHERE R.last_update > DATE_SUB(NOW(), INTERVAL 1 WEEK) AND R.site_id=S.Site_id AND R.test_id=T.test_id AND S.name='%s' AND T.name='%s'"%(site, test)
        result = self.DB._query( selectSQL )
        return result

    def web_getSiteMonthAvailability(self):
            self.DB = SAMDB()
            site = self.request.arguments['site'][0]
            test = self.request.arguments['test'][0]
            result = self.selectFromDB(site, test)
            if result['OK']:
                toSend = []
                previous = None
                for st in result['Value']:
                    if st[1] in STATE_MAP:
                        temp = {}
                        temp['time'] = str(st[0])
                        temp['state'] = getStateNumber(st[1])
                        temp['description'] = st[2]
                        toSend.append(temp)
                  
                self.write({"result":toSend})
            else:
                print 'Error during selecting from DB'
	

