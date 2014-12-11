########################################################################
# $HeadURL$
########################################################################
""" ProxyRepository class is a front-end to the proxy repository Database
"""

__RCSID__ = "0394cb5 (2012-10-23 15:23:42 +0200) Adri Casajs <adria@ecm.ub.es>"

import time, types
from DIRAC  import gConfig, gLogger, S_OK, S_ERROR
from DIRAC.Core.Utilities import Time
from DIRAC.Core.Base.DB import DB

class SAMDB( DB ):

  def __init__( self ):
    DB.__init__( self, 'SAMDB', 'Framework/SAMDB', 10 )
    retVal = self.__initializeDB()
    if not retVal[ 'OK' ]:
      raise Exception( "Can't create tables: %s" % retVal[ 'Message' ] )

  def __initializeDB( self ):
    """
    Create the tables
    """
    self.__permValues = [ 'USER', 'GROUP', 'VO', 'ALL' ]
    self.__permAttrs = [ 'ReadAccess' ]
    retVal = self._query( "show tables" )
    if not retVal[ 'OK' ]:
      return retVal

    tablesInDB = [ t[0] for t in retVal[ 'Value' ] ]
    tablesD = {}

    if 'Sites' not in tablesInDB:
      tablesD[ 'Sites' ] = { 'Fields' : { 'site_id' : 'INTEGER AUTO_INCREMENT NOT NULL',
                                          'name' : 'VARCHAR(32) NOT NULL'
                                            },
                                        'PrimaryKey' : 'site_id',
                                      }

    if 'Tests' not in tablesInDB:
      tablesD[ 'Tests' ] = { 'Fields' : { 'test_id' : 'INTEGER AUTO_INCREMENT NOT NULL',
                                          'name' : 'VARCHAR(128) NOT NULL',
                                          'executable' : 'VARCHAR(256) NOT NULL',
                                          'timeout' : 'INTEGER NOT NULL',
                                          'period' : 'INTEGER NOT NULL',
                                          'description' : 'TEXT'
                                        },
                                        'PrimaryKey' : 'test_id',
                                      }

    if 'SiteTests' not in tablesInDB:
      tablesD[ 'SiteTests' ] = { 'Fields' : { 'test_id' : 'INTEGER NOT NULL',
                                              'site_id' : 'INTEGER NOT NULL',
                                              'state' : 'VARCHAR(32) NOT NULL',
                                              'last_run' : 'DATETIME NOT NULL',
                                              'arguments' : 'TEXT'
                                            },
                                        'PrimaryKey' : ['test_id', 'site_id']
                                      }

    if 'Results' not in tablesInDB:
      tablesD[ 'Results' ] = { 'Fields' : { 'result_id' : 'INTEGER AUTO_INCREMENT NOT NULL',
                                            'test_id' : 'INTEGER NOT NULL',
                                            'site_id' : 'INTEGER NOT NULL',
                                            'wms_job_id' : 'INTEGER',
                                            'state' : 'VARCHAR(32) NOT NULL',
                                            'description' : 'VARCHAR(256)',
                                            'last_update' : 'DATETIME NOT NULL'
                                            },
                                        'PrimaryKey' : 'result_id',
                                      }


    if 'States' not in tablesInDB:
      tablesD[ 'States' ] = { 'Fields' : { 'site_id' : 'INTEGER NOT NULL',
                                           'test_id' : 'INTEGER NOT NULL',
                                           'result_id' : 'INTEGER NOT NULL'
                                       },             
                                        'PrimaryKey' : ['site_id', 'test_id']
                                      }

    return self._createTables( tablesD )
  
  def getTestsToRun(self):
    selectSQL = "SELECT S.name, S.site_id, T.executable, ST.last_run, ST.timeout, ST.arguments, T.test_id FROM SiteTests ST, Sites S, Tests T WHERE ST.state='Finished' AND ST.test_id=T.test_id AND ST.site_id=S.site_id"
    result = self._query( selectSQL )
    if not result[ 'OK' ]:
      return result
    print result['Value']
    return result
    
  def getRunningTests(self):
    selectSQL = "SELECT R.result_id, R.wms_job_id, R.last_update, ST.test_id FROM SiteTests ST, Results R WHERE R.state='JobSended' AND TtS.service_id=R.service_id AND TtS.test_id=R.test_id"
    result = self._query( selectSQL )
    if not result[ 'OK' ]:
      return result
    print result['Value']
    return result

  def setResult(self, result, result_id, description="", hostname="None"):
    sqlUpdate = "UPDATE Results SET state='%s', last_update=%s, description='%s' WHERE result_id=%s" % (result, "NOW()", description, result_id)
    gLogger.info(sqlUpdate)
    result = self._update( sqlUpdate )
    if not result['OK']:
      gLogger.error('Failed to fill the result row')
      return result

    selectSQL = "SELECT R.site_id, R.test_id FROM Results R, Services S WHERE R.site_id=S.site_id AND R.result_id=%s" % (result_id)
    result = self._query( selectSQL )
    if not result[ 'OK' ]:
      gLogger.error('Failed to et site_id and test_id')
      return result

    site_id, test_id =  int(result['Value'][0][0]), int(result['Value'][0][1])
    sqlUpdate = "UPDATE States SET result_id=%s  WHERE site_id=%s AND test_id=%s" % (result_id, site_id, test_id)
    result = self._update( sqlUpdate )
    if not result['OK']:
      gLogger.error('Failed to uodate UI with new test data')
      return result

    sqlUpdate = "UPDATE SiteTests SET state='%s' WHERE site_id=%s AND test_id=%s" % ("Finished", service_id, test_id)
    result = self._update( sqlUpdate )
    gLogger.info(result)
    if not result['OK']:
      return result

  def setLog(self, result_id, codeout, stdout):
    sqlSelect = "SELECT R.job_id from Results R where R.result_id=%s" % (result_id)
    job_id = self._query( sqlSelect )['Value'][0][0]
    if job_id==None:
       gLogger.error("Log request of Result with no registered job")
       return False
    sqlInsert = "INSERT INTO Logs (job_id, codeout, stdout) VALUES(%s, '%s', '%s')" % (job_id, codeout, stdout)
    result = self._update( sqlInsert )
    return result['Value']


  def createNewResult(self, test_id, site_id):
    sqlInsert = "INSERT INTO Results (test_id, site_id, last_update, state) VALUES (%s, %s, %s, '%s')" % (test_id, site_id, "NOW()",'initiated')
    result = self._update( sqlInsert )
    if not result['OK']:
      return result
    result_id = result['lastRowId']
    sqlUpdate = "UPDATE SiteTests SET state='%s', SiteTests.last_run=%s WHERE test_id=%s AND site_id=%s" % ('Running', "NOW()", test_id, service_id)
    result = self._update( sqlUpdate )
    if not result['OK']:
      return result
    return S_OK(result_id)

  def createJob(self, wms_job_id, result_id):
    sqlInsert = "UPDATE Results set wms_job_id=%s, last_update=%s, state=%s where result_id=%s" % (wms_job_id, "NOW()", "JobSended", result_id)
    result = self._update( sqlInsert )
    if not result['OK']:
      return result
    return S_OK(result)


  def getState(self):
    #selectSQL = "SELECT s.name, se.name, t.name, r.state, r.description FROM States st, Sites s, Services se, Tests t, Results r WHERE s.site_id=se.site_id AND se.service_id=st.service_id AND r.result_id=st.result_id"
    #selectSQL = "SELECT s.name, se.name, t.name, r.state, r.description, r.result_id, r.last_update, (select count(*)/(SELECT count(*) FROM Results WHERE service_id=se.service_id and test_id=t.test_id) AS Probability FROM Results WHERE state='Success' and service_id=se.service_id and test_id=t.test_id) FROM States st, Sites s, Services se, Tests t, Results r WHERE s.site_id=se.site_id AND se.service_id=st.service_id AND r.result_id=st.result_id;"
    #selectSQL = "SELECT s.name, se.name, t.name, r.state, r.description, r.result_id, r.last_update, (select count(*)/(SELECT count(*) FROM Results WHERE service_id=se.service_id and test_id=t.test_id) AS Probability FROM Results WHERE state='Success' and service_id=se.service_id and test_id=t.test_id) as Probability FROM States st, Sites s, Services se, Tests t, Results r WHERE s.site_id=se.site_id AND se.service_id=st.service_id AND r.result_id=st.result_id AND t.test_id=r.test_id;"
    selectSQL = "SELECT s.name, t.name, r.state, r.description, r.result_id, r.last_update, (SELECT count(*)/(SELECT count(*) FROM Results WHERE site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 24 HOUR)) FROM Results WHERE state='Success' and site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 24 HOUR)) as dayStat,(SELECT count(*)/(SELECT count(*) FROM Results WHERE site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 48 HOUR)) FROM Results WHERE state='Success' and site_id=se.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 48 HOUR)) as twoStat,(SELECT count(*)/(SELECT count(*) FROM Results WHERE site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 168 HOUR)) FROM Results WHERE state='Success' and site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 168 HOUR)) as weekStat FROM States st, Sites s, Tests t, Results r WHERE s.site_id=st.site_id AND r.result_id=st.result_id AND t.test_id=r.test_id;"
    print selectSQL
    result = self._query( selectSQL )
    print result['Value']
    return result

  def getSiteHistory(self, site):
    selectSQL = "SELECT r.last_update, r.state FROM Services se, Sites s, Results r WHERE s.name='%s' AND s.site_id=se.site_id AND r.service_id=se.service_id;" % site
    result = self._query( selectSQL )
    return result


  def getSiteMonthAvailability(self, site):
    selectSQL = "SELECT t.Date, t.Day, s.Success/t.Count  FROM (SELECT DATE(r.last_update) as Date, DAY(r.last_update) as Day, COUNT(r.last_update) as Success   FROM Results r, Services se, Sites s  WHERE s.name='%s' AND se.site_id=s.site_id AND r.service_id=se.service_id AND r.state='Success'  GROUP BY DAY(last_update) ORDER BY last_update ASC) s, (SELECT DATE(r.last_update) as Date, DAY(r.last_update) as Day, COUNT(r.last_update) as Count   FROM Results r, Services se, Sites s  WHERE s.name='%s' AND se.site_id=s.site_id AND r.service_id=se.service_id GROUP BY DAY(last_update) ORDER BY last_update ASC) t WHERE t.Date=s.Date ORDER BY t.Date ASC" % (site, site)
    result = self._query( selectSQL )
    return result
