########################################################################
# $HeadURL$
########################################################################

"""  GeneralPurposeAgent alow to run arbitrary commands by purpose or schedule.
"""
from DIRAC                                                  import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.Core.Base.AgentModule                            import AgentModule
from DIRAC.FrameworkSystem.DB.GeneralPurposeDB              import GeneralPurposeDB

__RCSID__ = '$Id:  $'

class GeneralPurposeAgent( AgentModule ):

    def initialize( self ):
        self.log.info( "initialize" )
        self.GPDB_dao = GeneralPurposeDB()
        return S_OK()

    def execute( self ):
        self.log.info( "execute" )
        x = PingCommand()
        x.execute()
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

class Command():

    def __init__( self, options = None):
        self.options = options

    def execute(self):
        return S_OK()

class PingCommand():

    def execute(self):

        def work(x):
            self.log.info(x)
            return x

        from multiprocessing import Pool

        WORK = [38, 39, 40, 41, 42, 41, 40]
        p = Pool(3)
        print p.map(work, WORK)
