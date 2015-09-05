from DIRAC import S_OK, S_ERROR, gLogger, gConfig
from DIRAC.Core.DISET.RPCClient                     import RPCClient
from DIRAC.Core.Utilities.ThreadSafe                import Synchronizer

gMonSynchro = Synchronizer()

class SAMClient:
  """
   TestClient
  """

  def __getRPCClient( self ):
    print 'here'
    return RPCClient( "Framework/SAM", timeout = 3600 )

  #@gMonSynchro
  def doTest( self, testType):
    """
    TestFunc
    """
    rpcClient = self.__getRPCClient()
    retVal = rpcClient.doTest( testType )
    return S_OK( retVal )
  
  #@gMonSynchro
  def setResult(self, result, result_id, description="", hostname="None"):    
    print "Client works"
    rpcClient = self.__getRPCClient()
    result = rpcClient.setResult(result, result_id, description, hostname)
    print result
    return S_OK()
 
  #@gMonSynchro
  def setHostStat(self, hostStat):
    rpcClient = self.__getRPCClient()
    result = rpcClient.setHostStat(hostStat)
    print result
    return S_OK()
 
  #@gMonSynchro
  def setNetStat(self, netStat):
    rpcClient = self.__getRPCClient()
    result = rpcClient.setNetStat(netStat)
    print result
    return S_OK()

  #@gMonSynchro
  def setDMSLatency(self, netStat):
    rpcClient = self.__getRPCClient()
    result = rpcClient.setDMSLatency(netStat)
    print result
    return S_OK()


