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

USE_PURE_MYSQL = True

def mysql_querry(querry):
  if USE_PURE_MYSQL:
    import MySQLdb
    db = MySQLdb.connect(host="diracdb.ihep.ac.cn", # your host, usually localhost
                         user="monitor", # your username
                         passwd="dirac4badger01", # your password
                         db="JobDB")
    cur = db.cursor()
    cur.execute(querry)
    data = cur.fetchall()
    cur.close()
    return data
  else:
    db = JobDB()
    return db._query( querry )['Value']

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
                
        result = mysql_querry( self.runningSQL )
        isOK = isOK and self.updateSending('running', result)
        
        result = mysql_querry( self.waitingSQL )
        isOK = isOK and self.updateSending('waiting', result)
            
        result = mysql_querry( self.failedSQL )
        isOK = isOK and self.updateSending('failed', result)
            
        result = mysql_querry( self.doneSQL )
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
