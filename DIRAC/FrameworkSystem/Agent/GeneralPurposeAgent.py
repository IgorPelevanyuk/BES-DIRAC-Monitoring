########################################################################
# $HeadURL$
########################################################################

"""  GeneralPurposeAgent alow to run arbitrary commands by purpose or schedule.
"""
from DIRAC                                                  import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.Core.Base.AgentModule                            import AgentModule
from DIRAC.FrameworkSystem.DB.GeneralPurposeDB              import GeneralPurposeDB
import subprocess

# DMStestCommand
from DIRAC.DataManagementSystem.Client.ReplicaManager       import ReplicaManager 
import os

__RCSID__ = '$Id:  $'

class GeneralPurposeAgent(AgentModule):

    def initialize(self):
        self.log.info("initialize")
        self.GPDB_dao = GeneralPurposeDB()
        return S_OK()

    def execute(self):
        self.log.info("execute")
        x = PingCommand()
        x.execute()
        return S_OK()
  
    def beginExecution(self):
        self.log.info("beginExecution")
    
        return S_OK()

    def endExecution(self):
        self.log.info("endExecution")

        return S_OK()

    def finalize(self):
        self.log.info("finalize")
    
        return S_OK()

class Command(object):

    def __init__(self):
        self.options = {}

    def execute(self):
        return S_OK()

class PingCECommand(Command):

    def __init__(self, options=None):
        super(PingCECommand, self).__init__()
        self.options.update(options)
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
        avgPingRaw = [i[1] for i in lines if i[0] == 'rtt']        #Returns the list with possible 'rtt' rest(should be ['xxx'](Success) or[](Fail))
        if len(avgPingRaw) != 0:
            avgPing = float(avgPingRaw[0].split('/')[4])     #Select only Avg and makes it float
        lossRaw = [i[1] for i in lines if 'packet loss' in i[1]]
        lossRaw = lossRaw[0].split(',')
        lossRaw = [i for i in lossRaw if 'packet loss' in i][0]
        loss = int(lossRaw.split('%')[0])
        passed = (100 - loss)*1.0/100
        return avgPing, passed, description

    def execute(self):
        hosts = self._get_host_list()
        for host in hosts:
            output, errors = self._get_ping_output(host)
            avgPing, passed, description = self._get_ping_stat(output)

class DMStestCommand(Command):

    def __init__(self, options=None):
        super(DMStestCommand, self).__init__()
        self.options['test_file'] = 'test_file.dat'
        self.options['lfn_path'] = '/bes/user/p/pelevanyuk/'
        self.options.update(options)
        self.command_type = 'dmstest'
        self.DB = GeneralPurposeDB()
        
    def _get_SEs(self):
        #TODO: implement the real functionality instead of the mock
        return ['IHEPD-USER', 'USTC-USER', 'JINR-USER']

    def _create_test_file(self, size=1):
        test_file = open(self.options['default_test_file'], 'w')
        test_file.write('b'*size)

    def _add_file(self, lfn, localfile, SE, guid=None):
        rm = ReplicaManager()
        self._create_test_file()
        if not os.path.exists(self.options['default_test_file']):
            gLogger.error("File %s must exist locally" % localfile)
        if not os.path.isfile(self.options['default_test_file']):
            gLogger.error("%s is not a file" % localfile)

        res = rm.putAndRegister(lfn, localfile, SE, guid)
        if not res['OK']:
            gLogger.error('Error: failed to upload %s to %s' % (lfn, SE))
            return S_ERROR(res['Message'])
        return S_OK(res['Value']['Successful'][lfn])

    def _remove_file(self, lfn):
        rm = ReplicaManager()
        res = rm.removeFile([lfn])
        if not res['OK']:
            gLogger.error("Failed to remove data", res['Message'])
            return res
        if lfn in res['Value']['Successful']:
            return S_OK(res['Value']['Successful'])
        return S_ERROR(res['Value']['Failed'])

    def _replicate(self, lfn, destinationSE, sourceSE="", localCache=""):
        rm = ReplicaManager()
        result = rm.replicateAndRegister(lfn, destinationSE, sourceSE, '', localCache)
        if not result['OK']:
            print 'ERROR %s' % (result['Message'])
            return result
        else:
            return S_OK(result['Value']['Successful'][lfn])

    def _get_file(self, lfn):
        rm = ReplicaManager()
        result = rm.getFile(lfn, "")
        if not result['OK']:
            return S_ERROR(result['Message'])

        if result['Value']['Failed']:
            return S_ERROR(result['Value'])
        return result

    def execute(self):
        SEs = self._get_SEs()
        results = {}
        descriptions = {}
        for se in SEs:
            upload_result = self._add_file(self.options['lfn'], self.options['test_file'], se)
            if upload_result['OK']:
                results[(se, se)] = upload_result['Value']['put']
                descriptions[(se, se)] = 'Success'
            else:
                results[(se, se)] = upload_result['Message']
                descriptions[(se, se)] = upload_result['Message']
                gLogger.info('Failed to upload the file to %s. Message: %s' % (se, upload_result['Message']))
            for destination in [x for x in SEs if x != se]:
                replicate_result = self._replicate(self.options['lfn'], destination)
                if replicate_result['OK']:
                    results[(se, destination)] = replicate_result['Value']['replicate']
                    descriptions[(se, destination)] = replicate_result['Message']
                else:
                    results[(se, destination)] = -1
                    descriptions[(se, destination)] = replicate_result['Message']
                    gLogger.info('Failed to replicate the file from %s to %s. Message: %s' % (se, destination, replicate_result['Message']))
            remove_result = self._remove_file(self.options['lfn'])
            if remove_result['OK']:
                descriptions[(se, se)] += 'Test file successfully removed'
            else:
                descriptions[(se, se)] += remove_result['Message']
                gLogger.info('Failed to remove file from %s. Message: %s' % (se, remove_result['Message']))

        gLogger.info(str(results))
        #for result in results:
         #   self.DB.addNewJournalRow(self.command_type, list(result), [results[result]], '')

