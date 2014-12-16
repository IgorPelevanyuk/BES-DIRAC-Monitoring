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
    
    def _updateSiteList(self):
        sitesInConfig = []
        sitesInDB = []
        #Calculate Max pledges for Cluster and GRIDs
        for directory in  gConfig.getSections('/Resources/Sites')['Value']:
            for site in gConfig.getSections('/Resources/Sites/'+directory)['Value']:
                sitesInConfig.append(site)
        dao = SAMDB()
        result = dao.getSiteList()
        if result['OK']:
            for site in result['Value']:
                sitesInDB.append(site[0])
        else:
            gLogger.error('Failed to update site list')
            return
        siteToAdd = []
        siteToDelete = []
        for site in sitesInConfig:
            if site not in sitesInDB:
                siteToAdd.append(site)
        for site in sitesInDB:
            if site not in sitesInConfig:
                siteToDelete.append(site)
        for site in siteToDelete:
            dao.deleteSite(site)
        for site in siteToAdd:
            dao.addNewSite(site)
        return S_OK()


    def _startNewTests(self):
        # Get list of tests
        testsToStart = []
        dao = SAMDB()
        result = dao.getTestsToStart()
        if not result['OK']:
            gLogger.error('Failed to load test to start')
        else:
            testsToStart = result['Value']

        # Create new Result db entity
        for test in testsToStart:
            site_id = test[0]
            test_id = test[1]
            site_name = test[2]
            test_name = test[3]
            executable = test[4]

            result = dao.startNewTest(site_id, test_id)
            if not result['OK']:
                break
            result_id = result['Value']
            executable = executable.split('&')
            gLogger.info("SEND Job: "+site_name+"  "+executable[0])
            dirac = Dirac()
            j = Job()
            j.setExecutable('python' , arguments = executable[0]+" "+str(result_id))
            j.setInputSandbox(['/opt/dirac/pro/DIRAC/FrameworkSystem/Agent/sam_tests/'+executable[0]])
            j.setName(test_name)
            j.setDestination( site_name )
            result = dirac.submit(j)
            if result['OK']:
                dao.addJobIdToResult(result_id, result['Value'])
            else:
                gLogger.error("Failed to submit the job: " + executable[0] + "to site "+site_name)
                dao.setResult('Fail', result_id, 'Failed to submit the job: '+str(result['Message']))
        return S_OK()

    def _stopOldTests(self):
        # Get list of tests
        testsToStop = []
        dao = SAMDB()
        result = dao.getTestsToStop()
        if not result['OK']:
            gLogger.error('Failed to load test to stop')
        else:
            testsToStop = result['Value']

        # Create new Result db entity
        for test in testsToStop:
            result_id = test[0]
            wms_job_id = test[1]
            timeout = test[2]

            dao.setResult('Fail', result_id, 'Timeout fail after '+str(timeout/60)+' min of silence')
          
            dirac = Dirac()
            result = dirac.delete(int(wms_job_id))

            if result['OK']:
                gLogger.info('Successfully killed the job with id: %s' % wms_job_id)
            else:
                gLogger.error("Failed to kill the job with id: %s" % wms_job_id )
        return S_OK()

    def initialize( self ):
        return S_OK()

    def execute( self ):
        self._startNewTests()
        self._stopOldTests()
        return S_OK()
  
    def beginExecution(self):
        self._updateSiteList()
        self.log.info( "CYCLE START!!" )
    
        return S_OK()

    def endExecution(self):
        self.log.info( "CYCLE STOP!!" )

        return S_OK()

    def finalize(self):
        self.log.info( "GRATEFUL EXIT. BYE" )
    
        return S_OK()
