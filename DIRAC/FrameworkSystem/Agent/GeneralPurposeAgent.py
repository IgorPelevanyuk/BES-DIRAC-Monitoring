########################################################################
# $HeadURL$
########################################################################

"""  GeneralPurposeAgent alow to run arbitrary commands by purpose or schedule.
"""
from DIRAC                                                  import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.Core.Base.AgentModule                            import AgentModule
from DIRAC.FrameworkSystem.DB.GeneralPurposeDB              import GeneralPurposeDB
import subprocess

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

class Command(object):

    def __init__(self, options=None):
        self.options = options

    def execute(self):
        return S_OK()

class PingCECommand(Command):

    def __init__(self, options=None):
        super(PingCECommand, self).__init__(options)
        self.command_type = 'pingce'

    def _get_host_list(self):
        #TODO: get data from configurations system
        pass

    def _get_ping_output(self, host):
        popen = subprocess.Popen(["ping", "-c 10", "-i 0.2", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = popen.communicate()
        output = result[0]
        errors = result[1]
        return output, errors

    def _get_ping_stat(self, output):
        description = ""
        avgPing = -1
        passed = -1

        if 'Packet filtered' in output:
            description = "Packets filtered"
        lines = output.split('\n')
        lines = [i.split(' ', 1) for i in lines]                #Splits line on the first word and the rest
        lines = [i for i in lines if len(i) == 2]                 #Filter empty lines
        avgPingRaw = [i[1] for i in lines if i[0]=='rtt']        #Returns the list with possible 'rtt' rest(should be ['xxx'](Success) or[](Fail) )
        if len(avgPingRaw)!=0:
            avgPing = float(avgPingRaw[0].split('/')[4])     #Select only Avg and makes it float
        lossRaw = [i[1] for i in lines if 'packet loss' in i[1]]
        lossRaw = lossRaw[0].split(',')
        lossRaw = [i for i in lossRaw if 'packet loss' in i][0]
        loss = int(lossRaw.split('%')[0])
        passed = (100 - loss)*1.0/100
        return avgPing, passed, description

    def execute(self):
        hosts = self._get_host_list()
        for host in host:
            output, errors = self._get_ping_output(host)
            avgPing, passed, description = self._get_ping_stat(output)
