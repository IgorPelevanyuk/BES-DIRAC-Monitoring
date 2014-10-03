########################################################################
# $HeadURL$
########################################################################
"""  LemonAgent reports the state of all installed and set up services and agents. This output is then
     used in lemon sensors.
"""
__RCSID__ = "c9278cc (2012-04-05 01:56:22 +0200) ricardo <Ricardo.Graciani@gmail.com>"

from DIRAC                                                  import gLogger, gConfig, S_OK
from DIRAC.Core.Base.AgentModule                            import AgentModule
from DIRAC.Interfaces.API.Job                               import Job
from DIRAC.Interfaces.API.Dirac                             import Dirac
from DIRAC.FrameworkSystem.DB.SAMDB                         import SAMDB
import os

class SAMCheckerAgent( AgentModule ):
  
  def initialize( self ):
    return S_OK()

  def execute( self ):
    """ Main execution method
    """
    # Get list of running jobs
    dao = SAMDB()
    runningTests = dao.getRunningTests()['Value']
    self.log.info(runningTests)
    # Leave only old
    testsToStop = []
    for test in runningTests:
      print test[2]
      timeout = 1800
      if test[3]==2:
        timeout = 5400
      if isTimeExceed(test[2], timeout):
        testsToStop.append(test)
    # Send JobKill through REST
    for test in testsToStop:
      result = deleteJob(test[1])
      timeout = 1800
      if test[3]==2:
        timeout = 5400
      if result:
        dao.setResult('Fail', test[0], 'Failed after '+str(timeout/60)+' min of silence')
    return S_OK()
  
  def beginExecution(self):
    self.log.info( "CYCLE START!!" )
    
    return S_OK()

  def endExecution(self):
    self.log.info( "CYCLE STOP!!" )

    return S_OK()

  def finalize(self):
    self.log.info( "GRATEFUL EXIT. BYE" )
    
    return S_OK()

import time
def getTimeNow():
  return long(time.time())

def toMySQLTime(time_epoch):
  stamp = time.localtime(time_epoch)
  return time.strftime('%Y-%m-%d %H:%M:%S', stamp)

def toEpochTime(mysql_time):
  stamp = time.strptime(mysql_time, "%Y-%m-%d %H:%M:%S")
  return long(time.mktime(stamp))
  
def isTimeExceed(lastTime, timeout):
  return getTimeNow()-long(lastTime.strftime('%s'))>timeout

import urllib
def deleteJob(wms_id):
  base = 'http://vm162.jinr.ru:8081/deleteJob/'
  url = base + str(wms_id) + '/'
  try:
    urllib.urlopen(url).read()
    print 'Job killed ', wms_id
    return True
  except:
    print 'Error during call to REST'
    return False
