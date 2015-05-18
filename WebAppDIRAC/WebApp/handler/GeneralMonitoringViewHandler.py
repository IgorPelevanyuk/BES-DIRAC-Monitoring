from WebAppDIRAC.Lib.WebHandler import WebHandler #@UnresolvedImport
from DIRAC import gLogger, S_OK, S_ERROR #@UnresolvedImport
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB #@UnresolvedImport

import math

def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp  

class GeneralMonitoringViewHandler(WebHandler):

    AUTH_PROPS = "all"
    toSend = {}
    defaultSite = {'running':0, 'waiting':0, 'failed':0, 'done':0}
    runningSQL = 'select Site, count(*) from Jobs where Status="Running" group by Site;'
    failedSQL = 'select Site, count(*) from Jobs where Status="Failed" group by Site;'
    doneSQL = 'select Site, count(*) from Jobs where Status="Done" group by Site;'
    waitingSQL = 'select Site, count(*) from Jobs where Status="Waiting" or Status="Checking" group by Site;'

    def updateSending(self, valueName, requestResult):
        if requestResult['OK']:            
            for row in requestResult['Value']:
                self.toSend[row[0]] = self.toSend.get(row[0], self.defaultSite.copy())
                self.toSend[row[0]][valueName] = row[1]
            return True
        else:
            gLogger.error('Failed to get info for %s due to: %s' % (valueName, requestResult['Message']))
            return False

    def selectFromDB(self):
        self.toSend = {}
        
        isOK = True
        jobDB = JobDB()
                
        result = jobDB._query( self.runningSQL )
        isOK = isOK and self.updateSending('running', result)
        
        result = jobDB._query( self.waitingSQL )
        isOK = isOK and self.updateSending('waiting', result)
            
        result = jobDB._query( self.failedSQL )
        isOK = isOK and self.updateSending('failed', result)
            
        result = jobDB._query( self.doneSQL )
        isOK = isOK and self.updateSending('done', result)       
        
        if isOK:
            return S_OK()
        else:
            return S_ERROR()

    def web_getData(self):
        gLogger.info('Get Data for general view')
        result = self.selectFromDB()
        if result['OK']:
            data = []
            for site in self.toSend:
                row = {}
                row['site'] = site
                row['running'] = self.toSend[site]['running']
                row['waiting'] = self.toSend[site]['waiting']
                row['failed'] = self.toSend[site]['failed']
                row['done'] = self.toSend[site]['done']
                data.append(row)
            self.write({"result":data})
        else:
            gLogger.error('Not possible to send overview data due to DB errors')
