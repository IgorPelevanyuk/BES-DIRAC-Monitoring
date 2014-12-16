########################################################################
# $HeadURL$
########################################################################
""" SAM database class. Provide all necessary functions for operations 
with tests.
"""

__RCSID__ = "0394cb5 (2012-10-23 15:23:42 +0200) Igor Pelevanyuk <>"

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
                                                'last_update' : 'DATETIME NOT NULL',
                                                'log' : 'TEXT'
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

    def addNewSite(self, site_name):
        # Add entry to the Sites table
        sqlInsert = "INSERT INTO Sites (name) VALUES ('%s')" % (site_name)
        result = self._update( sqlInsert )
        if not result[ 'OK' ]:
            gLogger.error('Failed to insert new site in addNewSite function')
            return result

        # Add entry to SiteTests
        site_id = result['lastRowId']
        sqlQuerry = "SELECT test_id from Tests"
        tests = self._query(sqlQuerry)['Value']
        for test_id in tests:
            sqlInsert = "INSERT INTO SiteTests (site_id, test_id, state, last_run) VALUES (%s, %s, '%s', DATE('1970-01-01'))" % (site_id, test_id[0], 'Waiting')
            result = self._update( sqlInsert )
            if not result[ 'OK' ]: 
                gLogger.error('Failed to match test %s for %s'%(test_id[0], site_id))
        return S_OK()

    def addNewTest(self, test_name, executable, period, timeout, description):
        # Add entry to Tests table
        sqlInsert = "INSERT INTO Tests (name, executable, period, timeout, description) VALUES ('%s', '%s', %s, %s, '%s')" % (test_name, executable, period, timeout, description )
        result = self._update( sqlInsert )
        if not result[ 'OK' ]:
            gLogger.error('Failed to insert new test in addNewTest function')
            return result

        # Add entry to SiteTests table
        test_id = result['lastRowId']
        sqlQuerry = "SELECT site_id from Sites"
        sites = self._query(sqlQuerry)['Value']
        for site_id in sites:
            sqlInsert = "INSERT INTO SiteTests (site_id, test_id, state, last_run) VALUES (%s, %s, '%s', DATE('1970-01-01'))" % (site_id[0], test_id, 'Waiting')
            result = self._update( sqlInsert )
            if not result[ 'OK' ]: 
                gLogger.error('Failed to match test %s for %s'%(test_id, site_id[0]))
        return S_OK()

    def deleteSite(self, site_name):
        # Get Id of required site
        sqlQuerry = "SELECT site_id from Sites WHERE name='%s'"%(site_name)
        result = self._query(sqlQuerry)
        if not result[ 'OK' ]:
            gLogger.error('Failed to find site_name %s' % (site_name))
            return result
        site_id = result['Value'][0]

        # Delete required site_id from SiteTests
        sqlDelete = "DELETE FROM SiteTests WHERE site_id=%s" % (site_id)
        result = self._transaction(sqlQuerry)
        if not result[ 'OK' ]:
            gLogger.error('Failed to delete site_id %s for site_name %s from SiteTests table' % (site_id, site_name))
            return result

        # Delete required site_id from Sites
        sqlDelete = "DELETE FROM Sites WHERE site_id=%s" % (site_id)
        result = self._transaction( sqlDelete )
        if not result[ 'OK' ]:
            gLogger.error('Failed to delete site_id %s for site_name %s from Sites table' % (site_id, site_name))
            return result

        # Delete site from UI
        sqlDelete = "DELETE FROM States WHERE site_id=%s" % (site_id)
        if not result[ 'OK' ]:
            gLogger.error('Failed to delete site_id %s for site_name %s from States table' % (site_id, site_name))
            return result
        return S_OK()

    def deleteTest(self, test_name):
        # Get Id of required test
        sqlQuerry = "SELECT test_id from Tests WHERE name='%s'"%(test_name)
        result = self._query(sqlQuerry)
        if not result[ 'OK' ]:
            gLogger.error('Failed to find test_name %s' % (test_name))
            return result
        test_id = result['Value'][0]

        # Delete required test_id from SiteTests
        sqlDelete = "DELETE FROM SiteTests WHERE test_id=%s" % (test_id)
        result = self._transaction(sqlQuerry)
        if not result[ 'OK' ]:
            gLogger.error('Failed to delete test_id %s for test_name %s from SiteTests table' % (test_id, test_name))
            return result

        # Delete required test_id from Tests
        sqlDelete = "DELETE FROM Tests WHERE test_id=%s" % (test_id)
        result = self._transaction( sqlDelete )
        if not result[ 'OK' ]:
            gLogger.error('Failed to delete test_id %s for test_name %s from Tests table' % (test_id, test_name))
            return result

        # Delete test from UI
        sqlDelete = "DELETE FROM States WHERE test_id=%s" % (test_id)
        if not result[ 'OK' ]:
            gLogger.error('Failed to delete test_id %s for test_name %s from States table' % (test_id, test_name))
            return result
        return S_OK()       

    def getTestsToStart(self):
        sqlSelect = "SELECT S.site_id, T.test_id, S.name, T.name, T.executable FROM SiteTests ST, Sites S, Tests T WHERE ST.state='Waiting' AND ST.test_id=T.test_id AND ST.site_id=S.site_id AND (UNIX_TIMESTAMP(UTC_TIMESTAMP())-UNIX_TIMESTAMP(ST.last_run))>T.period"
        result = self._query( sqlSelect )
        if not result[ 'OK' ]:
            gLogger.error('Failed to get tests to start')
            return result
        return result
    
    def getTestsToStop(self):
        sqlSelect = "SELECT R.result_id, R.wms_job_id, T.timeout FROM SiteTests ST, Results R, Tests T WHERE ST.status='Running'  AND ST.site_id=R.site_id AND ST.test_id=R.test_id AND R.status='JobSended' AND (UNIX_TIMESTAMP(UTC_TIMESTAMP())-UNIX_TIMESTAMP(ST.last_run))>T.timeout"
        result = self._query( sqlSelect )
        if not result[ 'OK' ]:
            gLogger.error('Failed to get tests to stop after timeout')
            return result
        return result

    def getSiteList(self):
    	sqlSelect = "SELECT name FROM Sites"
    	result = self._query( sqlSelect )
    	if not result[ 'OK' ]:
            gLogger.error('Failed to get site list')
            return result
        return result

    def changeSiteTestsStatus(self, site_id, test_id, status):
        sqlUpdate = "UPDATE SiteTests SET status='%s' WHERE site_id=%s AND test_id=%s" % (status, site_id, test_id)
        result = self._update( sqlUpdate )
        if not result[ 'OK' ]:
            gLogger.error('Failed to get tests to stop after timeout')
            return result
        return result

    def setResult(self, result, result_id, description=""):
        sqlUpdate = "UPDATE Results SET state='%s', last_update=%s, description='%s' WHERE result_id=%s" % (result, "UTC_TIMESTAMP()", description, result_id)
        gLogger.info(sqlUpdate)
        result = self._update( sqlUpdate )
        if not result['OK']:
            gLogger.error('Failed to set the result row')
            return result

        sqlSelect = "SELECT R.site_id, R.test_id FROM Results R WHERE R.result_id=%s" % (result_id)
        result = self._query( sqlSelect )
        if not result[ 'OK' ]:
            gLogger.error('Failed to get site_id and test_id')
            return result

        site_id, test_id =  int(result['Value'][0][0]), int(result['Value'][0][1])
        sqlUpdate = "INSERT INTO States (site_id, test_id, result_id) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE result_id=VALUES(result_id)" % (site_id, test_id, result_id)
        result = self._update( sqlUpdate )
        if not result['OK']:
            gLogger.error('Failed to update UI with new result')
            return result

        result = self.changeSiteTestsStatus(site_id, test_id, 'Waiting')
        if not result['OK']:
            gLogger.error('Failed to change state of SiteTest')
            return result

    def setLog(self, result_id, log):
        sqlInsert = "INSERT INTO Results (result_id, log) VALUES(%s, '%s')" % (result_id, log)
        result = self._update( sqlInsert )
        if not result['OK']:
            gLogger.error('Failed to add log for result_id %s' % result_id)
            return result
        return result

    def startNewTest(self, site_id, test_id):
        sqlInsert = "INSERT INTO Results (test_id, site_id, last_update, state) VALUES (%s, %s, %s, '%s')" % (test_id, site_id, "UTC_TIMESTAMP()",'Initiated')
        result = self._update( sqlInsert )
        if not result['OK']:
            gLogger.error('Failed to create new result entity')
            return result
        result_id = result['lastRowId']
        sqlUpdate = "UPDATE SiteTests SET state='%s', SiteTests.last_run=%s WHERE test_id=%s AND site_id=%s" % ('Running', "UTC_TIMESTAMP()", test_id, site_id)
        result = self._update( sqlUpdate )
        if not result['OK']:
            gLogger.error('Failed to update SiteTests status')
            return result
        return S_OK(result_id)

    def addJobIdToResult(self, result_id, wms_job_id):
        sqlInsert = "UPDATE Results set wms_job_id=%s, last_update=%s, state=%s where result_id=%s" % (wms_job_id, "UTC_TIMESTAMP()", "JobSended", result_id)
        result = self._update( sqlInsert )
        if not result['OK']:
            return result
        return result
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ REVISION LINE ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def getState(self):
        #sqlSelect = "SELECT s.name, se.name, t.name, r.state, r.description FROM States st, Sites s, Services se, Tests t, Results r WHERE s.site_id=se.site_id AND se.service_id=st.service_id AND r.result_id=st.result_id"
        #sqlSelect = "SELECT s.name, se.name, t.name, r.state, r.description, r.result_id, r.last_update, (select count(*)/(SELECT count(*) FROM Results WHERE service_id=se.service_id and test_id=t.test_id) AS Probability FROM Results WHERE state='Success' and service_id=se.service_id and test_id=t.test_id) FROM States st, Sites s, Services se, Tests t, Results r WHERE s.site_id=se.site_id AND se.service_id=st.service_id AND r.result_id=st.result_id;"
        #sqlSelect = "SELECT s.name, se.name, t.name, r.state, r.description, r.result_id, r.last_update, (select count(*)/(SELECT count(*) FROM Results WHERE service_id=se.service_id and test_id=t.test_id) AS Probability FROM Results WHERE state='Success' and service_id=se.service_id and test_id=t.test_id) as Probability FROM States st, Sites s, Services se, Tests t, Results r WHERE s.site_id=se.site_id AND se.service_id=st.service_id AND r.result_id=st.result_id AND t.test_id=r.test_id;"
        sqlSelect = "SELECT s.name, t.name, r.state, r.description, r.result_id, r.last_update, (SELECT count(*)/(SELECT count(*) FROM Results WHERE site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 24 HOUR)) FROM Results WHERE state='Success' and site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 24 HOUR)) as dayStat,(SELECT count(*)/(SELECT count(*) FROM Results WHERE site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 48 HOUR)) FROM Results WHERE state='Success' and site_id=se.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 48 HOUR)) as twoStat,(SELECT count(*)/(SELECT count(*) FROM Results WHERE site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 168 HOUR)) FROM Results WHERE state='Success' and site_id=s.site_id and test_id=t.test_id and last_update>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 168 HOUR)) as weekStat FROM States st, Sites s, Tests t, Results r WHERE s.site_id=st.site_id AND r.result_id=st.result_id AND t.test_id=r.test_id;"
        result = self._query( sqlSelect )
        print result['Value']
        return result

    def getSiteHistory(self, site):
        sqlSelect = "SELECT r.last_update, r.state FROM Services se, Sites s, Results r WHERE s.name='%s' AND s.site_id=se.site_id AND r.service_id=se.service_id;" % site
        result = self._query( sqlSelect )
        return result


    def getSiteMonthAvailability(self, site):
        sqlSelect = "SELECT t.Date, t.Day, s.Success/t.Count  FROM (SELECT DATE(r.last_update) as Date, DAY(r.last_update) as Day, COUNT(r.last_update) as Success   FROM Results r, Services se, Sites s  WHERE s.name='%s' AND se.site_id=s.site_id AND r.service_id=se.service_id AND r.state='Success'  GROUP BY DAY(last_update) ORDER BY last_update ASC) s, (SELECT DATE(r.last_update) as Date, DAY(r.last_update) as Day, COUNT(r.last_update) as Count   FROM Results r, Services se, Sites s  WHERE s.name='%s' AND se.site_id=s.site_id AND r.service_id=se.service_id GROUP BY DAY(last_update) ORDER BY last_update ASC) t WHERE t.Date=s.Date ORDER BY t.Date ASC" % (site, site)
        result = self._query( sqlSelect )
        return result
