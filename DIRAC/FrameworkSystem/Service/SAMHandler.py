# $HeadURL$
__RCSID__ = "3e8fb84 (2011-02-18 15:45:18 +0000) Ricardo Graciani <graciani@ecm.ub.es>"
import types
from DIRAC import S_OK, S_ERROR, gConfig, gLogger #@UnresolvedImport
from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB
from DIRAC.Core.DISET.RequestHandler import RequestHandler #@UnresolvedImport

import urllib
import json
def getLogs(wms_id):
  base = 'http://vm162.jinr.ru:8081/getLogs/'
  url = base + wms_id + '/'
  try:
    logs = urllib.urlopen(url).read()
    logs = json.loads(logs)
    print 'Logs received'
  except:
    logs = False
  return logs

def initializeSAMHandler( serviceInfo ):
  global gSAMDB
  gSAMDB = SAMDB()
  return S_OK()

class SAMHandler( RequestHandler ):
  types_doTest = [ types.StringType ]
  def export_doTest( self, typeName ):
    """
      Add a record for a type
    """
    self.log = gLogger.getSubLogger('Test Successfull')
    self.log.info('CALL')
    self.log.info(typeName)
    return S_OK("Return value")
  
  types_setResult = [ types.StringType, types.IntType, types.StringType ]
  def export_setResult(self, result, result_id, description="", hostname='None'):
    """
      Set result for a particular result_id
    """
    self.log = gLogger.getSubLogger('')
    self.log.info('Result ' + result + ' for ' + str(result_id) + ' has been received' )
    result = gSAMDB.setResult(result, result_id, description, hostname)
    
    self.log.info(str(result))
    return S_OK(result)

  types_setHostStat = [ types.ListType ]
  def export_setHostStat(self, hostStat):
    """
      Set result for hostStat
    """
    self.log = gLogger.getSubLogger('HostStat received')
    gSAMDB.setHostStat(hostStat)
    return S_OK()
    
  types_setNetStat = [ types.ListType ]
  def export_setNetStat(self, netStat):
    """
      Set result for netStat
    """
    self.log = gLogger.getSubLogger('NetStat received')
    gSAMDB.setNetStat(netStat)
    return S_OK()
  
  types_setDMSLatency = [ types.ListType ]
  def export_setDMSLatency(self, dmsLatency):
    """
      Set result for DMS Latency
    """
    self.log = gLogger.getSubLogger('DMSLatency received')
    gSAMDB.setDMSLatency(dmsLatency)
    return S_OK()
