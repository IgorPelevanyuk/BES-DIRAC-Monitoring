from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB
from DIRAC import gConfig

import math

def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp

USE_PURE_MYSQL = True

def mysql_querry(querry, DB):
    if USE_PURE_MYSQL:
        import MySQLdb
        db = MySQLdb.connect(host="diracdb.ihep.ac.cn",
                         user="monitor",
                         passwd="dirac4badger01",
                         db=DB)
        cur = db.cursor()
        cur.execute(querry)
        data = cur.fetchall()
        cur.close()
        return S_OK(data)
    else:
        db = JobDB()
        return db._query( querry )['Value']

def getSEs():
    siteSEs = []
    SEs = {}
    for se in gConfig.getSections('/Resources/StorageElements')['Value']:
        SEs[se] = gConfig.getValue('/Resources/StorageElements/'+se+'/AccessProtocol.1/Host')
        # print se, ': ', SEs[se]
    for dir in gConfig.getSections('/Resources/Sites')['Value']:
        for site in gConfig.getSections('/Resources/Sites/'+dir)['Value']:
            if 'SE' in gConfig.getOptions('/Resources/Sites/'+dir+'/'+site)['Value']:
                siteSEs.append((site, gConfig.getValue('/Resources/Sites/'+dir+'/'+site+'/SE')))
            # print site, ': ', siteSEs[site], ' : ', SEs[siteSEs[site]] if siteSEs[site]!='' else ''
    return siteSEs

def getSEtoSite():
    siteSEs = dict([(x[1], x[0]) for x in getSEs()])


class GeneralMonitoringViewHandler(WebHandler):

    AUTH_PROPS = "all"
    toSend = {}
    defaultSite = {'running': 0, 'waiting': 0, 'failed': 0, 'done': 0, 'se': '', 'sesize': 0}
    runningSQL = 'select Site, count(*) from Jobs where Status="Running" group by Site;'
    failedSQL = 'select Site, count(*) from Jobs where Status="Failed" group by Site;'
    doneSQL = 'select Site, count(*) from Jobs where Status="Done" group by Site;'
    waitingSQL = 'select Site, count(*) from Jobs where Status="Waiting" or Status="Checking" group by Site;'
    dataOnSEsSQL = 'select SE.SEName, sum(F.Size) from FC_Replicas R, FC_Files F, FC_StorageElements SE where R.FileID=F.FileID and R.SEID=SE.SEID group by R.SEID;'

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

        result = mysql_querry(self.runningSQL, 'JobDB')
        isOK = isOK and self.updateSending('running', result)

        result = mysql_querry(self.waitingSQL, 'JobDB')
        isOK = isOK and self.updateSending('waiting', result)

        result = mysql_querry(self.failedSQL, 'JobDB')
        isOK = isOK and self.updateSending('failed', result)

        result = mysql_querry(self.doneSQL, 'JobDB')
        isOK = isOK and self.updateSending('done', result)

        result = getSEs()
        isOK = isOK and self.updateSending('se', S_OK(result))

        siteSize = getSEs()
        seSize = {}
        result = mysql_querry(self.dataOnSEsSQL, 'FileCatalogDB')
        for row in result['Value']:
            seSize[row[0]] = row[1]
        for site in siteToSE:
            site[1] = seSize[site[1]]
        isOK = isOK and self.updateSending('sesize', S_OK(siteSize))

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
                row['se'] = self.toSend[site]['se']
                row['sesize'] = self.toSend[site]['sesize']
                data.append(row)
            self.write({"result": data})
        else:
            gLogger.error('Not possible to send overview data due to DB errors')
