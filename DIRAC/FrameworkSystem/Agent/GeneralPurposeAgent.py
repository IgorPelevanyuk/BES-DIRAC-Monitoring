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
        self.GPDB_dao = GeneralPurposeDB()
        return S_OK()

    def execute( self ):
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
