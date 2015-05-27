########################################################################
# $HeadURL$
########################################################################

"""  GeneralPurposeAgent alow to run arbitrary commands by purpose or schedule.
"""
from DIRAC                                                  import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.Core.Base.AgentModule                            import AgentModule
from DIRAC.FrameworkSystem.DB.GeneralPurposeDB              import GeneralPurposeDB

class GeneralPurposeAgent( AgentModule ):

    def initialize( self ):
        self.log.info( "initialize" )
        self.GPDB_dao = GeneralPurposeDB()
        return S_OK()

    def execute( self ):
        self.log.info( "execute" )
        return S_OK()
  
    def beginExecution(self):
        self.log.info( "beginExecution" )
    
        return S_OK()

    def endExecution(self):
        self.log.info( "endExecution" )

        return S_OK()

    def finalize(self):
        self.log.info( "finalize" )
    
        return S_OK()
