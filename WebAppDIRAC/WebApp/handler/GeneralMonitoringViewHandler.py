from WebAppDIRAC.Lib.WebHandler import WebHandler
from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB
from DIRAC import gConfig

import math
import json

def trunc(float_num):
    '''Truncates/pads a float float_num to n decimal places without rounding'''
    temp = float_num * 100
    temp = math.floor(temp)
    temp = temp / 100
    return temp

USE_PURE_MYSQL = True

def mysql_querry(querry, db_name, mysql_host='diracdb.ihep.ac.cn'):
    if USE_PURE_MYSQL:
        import MySQLdb
        dba_object = MySQLdb.connect(host=mysql_host,
                         user="monitor",
                         passwd="###DIRAC_DB_PASS###",
                         db=db_name)
        cur = dba_object.cursor()
        cur.execute(querry)
        data = cur.fetchall()
        cur.close()
        return S_OK(data)
    else:
        dba_object = JobDB()
        return dba_object._query( querry )['Value']

def getSiteToSEmapping():
    """ Return the list of list(pairs) [[site, dedicated_se], [site, dedicated_se]] """
    siteSEs = []
    SEs = {}
    for se in gConfig.getSections('/Resources/StorageElements')['Value']:
        SEs[se] = gConfig.getValue('/Resources/StorageElements/'+se+'/AccessProtocol.1/Host')
    for section in gConfig.getSections('/Resources/Sites')['Value']:
        for site in gConfig.getSections('/Resources/Sites/'+section)['Value']:
            if 'SE' in gConfig.getOptions('/Resources/Sites/'+section+'/'+site)['Value']:
                siteSEs.append([site, gConfig.getValue('/Resources/Sites/'+section+'/'+site+'/SE')])
    return siteSEs

class GeneralMonitoringViewHandler(WebHandler):

    AUTH_PROPS = "all"
    to_send = {}
    defaultSite = {'running': 0, 'waiting': 0, 'failed': 0, 'done': 0, 'se': '', 'sesize': 0}
    runningSQL = 'select Site, count(*) from Jobs where Status="Running" group by Site;'
    failedSQL = 'select Site, count(*) from Jobs where Status="Failed" group by Site;'
    doneSQL = 'select Site, count(*) from Jobs where Status="Done" group by Site;'
    waitingSQL = 'select Site, count(*) from Jobs where Status="Waiting" or Status="Checking" group by Site;'
    dataOnSEsSQL = 'select SE.SEName, sum(F.Size) from FC_Replicas R, FC_Files F, FC_StorageElements SE where R.FileID=F.FileID and R.SEID=SE.SEID group by R.SEID;'
    seStatusSQL = 'select key_json, result_json, description from Journal J INNER JOIN (select row_type, key_json, max(insert_time) as insert_time from Journal where insert_time>=DATE_SUB(UTC_TIMESTAMP(),INTERVAL 2 HOUR) and row_type="dmstest" group by row_type, key_json) as max using(row_type, key_json, insert_time);'

    def updateSending(self, value_name, request_result):
        """ Update currend dictionary for sending. Accepts request_result as 
        a list of pairs (site, value) under the wrapper of S_OK(). 
        value_name is just a key for the dictionary"""
        if request_result['OK']:
            for row in request_result['Value']:
                self.to_send[row[0]] = self.to_send.get(row[0], self.defaultSite.copy())
                self.to_send[row[0]][value_name] = row[1]
            return True
        else:
            gLogger.error('Failed to get info for %s due to: %s' % (value_name, request_result['Message']))
            return False

    def selectFromDB(self):
        self.to_send = {}

        is_ok = True

        result = mysql_querry(self.runningSQL, 'JobDB')
        is_ok = is_ok and self.updateSending('running', result)

        result = mysql_querry(self.waitingSQL, 'JobDB')
        is_ok = is_ok and self.updateSending('waiting', result)

        result = mysql_querry(self.failedSQL, 'JobDB')
        is_ok = is_ok and self.updateSending('failed', result)

        result = mysql_querry(self.doneSQL, 'JobDB')
        is_ok = is_ok and self.updateSending('done', result)

        result = getSiteToSEmapping()
        is_ok = is_ok and self.updateSending('se', S_OK(result))

        site_size = []
        se_size = {}
        result = mysql_querry(self.dataOnSEsSQL, 'FileCatalogDB')
        for row in result['Value']:
            se_size[row[0]] = row[1]
        for (site, se) in getSiteToSEmapping():
            site_size.append((site, se_size[se]))
        is_ok = is_ok and self.updateSending('sesize', S_OK(site_size))

        se_status = {}
        site_se_status = []
        result = mysql_querry(self.seStatusSQL, 'GeneralPurposeDB', 'localhost')
        for row in result['Value']:
            key_val = json.loads(row[0])
            if len(set(key_val)) == 1: # If there is two same SE in the key_val
                se_status[key_val[0]] = json.loads(row[1])[0]
        for (site, se) in getSiteToSEmapping():
            site_se_status.append((site, se_status.get(se, 'Fail')))
        is_ok = is_ok and self.updateSending('sestatus', S_OK(site_se_status))

        if is_ok:
            return S_OK()
        else:
            return S_ERROR()

    def web_getData(self):
        gLogger.info('Get Data for general view')
        result = self.selectFromDB()
        if result['OK']:
            data = []
            for site in self.to_send:
                row = {}
                row['site'] = site
                row['running'] = self.to_send[site]['running']
                row['waiting'] = self.to_send[site]['waiting']
                row['failed'] = self.to_send[site]['failed']
                row['done'] = self.to_send[site]['done']
                row['se'] = self.to_send[site]['se']
                row['sesize'] = trunc(self.to_send[site]['sesize']/1024/1024/1024)
                row['sestatus'] = self.to_send[site]['sestatus']
                data.append(row)
            self.write({"result": data})
        else:
            gLogger.error('Not possible to send overview data due to DB errors')
