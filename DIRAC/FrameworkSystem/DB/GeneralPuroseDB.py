########################################################################
# $HeadURL$
########################################################################
""" GeneralPurposeDB main class. This database is intended to use in 
cases when it is not enough to use only SAMDB.
"""

__RCSID__ = "0394cb5 (2012-10-23 15:23:42 +0200) Igor Pelevanyuk <>"

from DIRAC  import gLogger, S_OK, S_ERROR
from DIRAC.Core.Base.DB import DB

class GeneralPurposeDB(DB):

    def __init__(self):
        DB.__init__(self, 'GeneralPurposeDB', 'Framework/GeneralPurposeDB', 10)
        retVal = self.__initializeDB()
        if not retVal['OK']:
            raise Exception("Can't create tables: %s" % retVal['Message'])

    def __initializeDB(self):
        """
        Create the tables
        """
        self.__permValues = ['USER', 'GROUP', 'VO', 'ALL']
        self.__permAttrs = ['ReadAccess']
        retVal = self._query("show tables")
        if not retVal['OK']:
            return retVal

        tablesInDB = [t[0] for t in retVal['Value']]
        tablesD = {}

        if 'Journal' not in tablesInDB:
            tablesD['Journal'] = {'Fields': {'journal_id' : 'INTEGER AUTO_INCREMENT NOT NULL',
                                             'type' : 'VARCHAR(128) NOT NULL',
                                             'time' : 'DATETIME NOT NULL',
                                             'key' : 'TEXT',
                                             'result': 'TEXT',
                                             'description': 'TEST'
                                        },
                                           'PrimaryKey' : 'journal_id',
                                 }

        return self._createTables(tablesD)

    def addNewJournalRow(self, row_type, key_list, result_list, description):
        """ Add onw new row to the GeneralPurposeDB.Journal table. 
        In case of problems return S_ERROR and logs the reason"""

        sqlInsert = "INSERT INTO Journal (type, time, key, result, description) VALUES ('%s',%s,'%s','%s','%s')" % (row_type, 'UTC_TIMESTAMP()', key_list, result_list, description)
        result = self._update(sqlInsert)
        if not result['OK']:
            gLogger.error('Failed to insert new row in addNewJournalRow function: %s.' % result['Message'])
        return result

    def getAllLatestResults(self, period):
        """ Returns the list of rows of all types for the last <period> hours."""

        if not isinstance(period, int):
            gLogger.error('<period> variable is not an instance of integer')
            return S_ERROR('<period> variable is not an instance of integer')

        sqlQuerry = "SELECT type, time, key, result, description from Journal WHERE time >= DATE_SUB(UTC_TIMESTAMP(),INTERVAL %s HOUR)" % (str(period))
        result = self._query(sqlQuerry)
        if not result['OK']:
            gLogger.error('Failed to get Latest Results from Journal: %s' % result['Message'])
            return result

        return S_OK()

    def getResults(self, row_type, period):
        """ Returns the list of rows of a particular type for the last <period> hours."""

        if not isinstance(period, int):
            gLogger.error('<period> variable is not an instance of integer')
            return S_ERROR('<period> variable is not an instance of integer')

        sqlQuerry = "SELECT type, time, key, result, description from Journal WHERE type='%s' and time >= DATE_SUB(UTC_TIMESTAMP(),INTERVAL %s HOUR)" % (row_type, str(period))
        result = self._query(sqlQuerry)
        if not result['OK']:
            gLogger.error('Failed to get Latest Results from Journal: %s' % result['Message'])
            return result

        return S_OK()

    def cleanDB(self):
        """ Removes all the data which is older then """
        return S_OK()
