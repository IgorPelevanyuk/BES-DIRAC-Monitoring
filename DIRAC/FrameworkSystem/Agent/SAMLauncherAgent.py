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
class SAMLauncherAgent( AgentModule ):

  def initialize( self ):
    return S_OK()

  def execute( self ):
    """ Main execution method
    """
    self.log.info( "    TICK!!" )
    self.log.info( self.am_getOption("PollingTime") )
    # Get list of tests
    dao = SAMDB()
    testList = dao.getTestsToRun()['Value']
    print testList
    # Leave only old and Finished
    testsToRun = []
    for test in testList:
      self.log.info(str(test[3])+"  "+str(test[4]))
      self.log.info(str(getTimeNow())+"  "+str(long(test[3].strftime('%s'))))
      self.log.info(getTimeNow()-long(test[3].strftime('%s')))

      if isTimeExceed(test[3], test[4]):
        self.log.info(str(test[3])+"  "+str(test[4]))
        self.log.info(str(getTimeNow())+"  "+str(long(test[3].strftime('%s'))))
        self.log.info(getTimeNow()-long(test[3].strftime('%s')))
        testsToRun.append(test)
    # Create new Result db entity
    for test in testsToRun:
      result_id = dao.createNewResult(test[6], test[7])
      wms_id = sendJob(test[0], test[2], result_id['Value'])
      print 'wms_id ',  wms_id
      if wms_id != 0:
        dao.createJob(wms_id,test[6], result_id['Value'])
      else:
        dao.setResult('Fail', result_id['Value'], 'Failed to submit the job')
    # Try to send job
      #IF failed to get job_id - mark FAIL
      #NEXT
    # Create Job db entity
    # Update result
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
  stamp = time.gmtime(time_epoch)
  return time.strftime('%Y-%m-%d %H:%M:%S', stamp)

def toEpochTime(mysql_time):
  stamp = time.strptime(mysql_time, "%Y-%m-%d %H:%M:%S")
  return long(time.mktime(stamp))
  
def isTimeExceed(lastTime, timeout):
  return getTimeNow()-long(lastTime.strftime('%s'))>timeout

import urllib
def sendJob(site, executable, result_id):
  base = 'http://vm162.jinr.ru:8081/sendJob/'
  url = base + site + '/' + executable + '/' + str(result_id)+'/'
  try:
    wms_id = urllib.urlopen(url).read()
    print 'from rest ', wms_id
  except:
    wms_id = 0
  return int(wms_id)
