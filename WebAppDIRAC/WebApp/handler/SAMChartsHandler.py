from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB

import math


STATE_MAP = {'Success':5,
             'Timeout':4,
             'Banned':1,
             'Fail':0,}
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

class SAMChartsHandler(WebHandler):

    AUTH_PROPS = "all"

    def selectFromDB(site, test):
        selectSQL = "SELECT unix_timestamp(R.last_update), R.state FROM Results R, Sites S, Tests T WHERE R.site_id=S.Site_id AND R.test_id=T.test_id AND S.name='%s' AND T.name='%s'"%(site, test)
        result = self.DB._query( selectSQL )
        return result
    
    def web_getSiteMonthAvailability(self):
            self.DB = SAMDB()
            site = self.request.arguments['site'][0]
            test = self.request.arguments['test'][0]
            result = self.selectFromDB(site, test)
            if result['OK']:
                print result['Value']
                toSend = []
                previous = None
                for st in result['Value']:
                    temp = {}
                    temp['time'] = st[0]
                    
                    state = getStateNumber(st[1])
                    if state == STATE_MAP['Success'] or state == STATE_MAP['Fail']:
                        previous = state
                    if state == STATE_MAP['Banned']:
                        previous = None
                    #if state == STATE_MAP['Timeout'] and previous!=None:
                    #    state = previous
                    temp['state'] = state
                    toSend.append(temp)
                self.write({"result":result})
            else:
                print 'Error during selecting from DB'

