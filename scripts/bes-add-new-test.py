from DIRAC import S_OK, S_ERROR, gLogger, gConfig, exit
from DIRAC.Core.Base import Script
Script.parseCommandLine( ignoreErrors = False )

from DIRAC.FrameworkSystem.DB.SAMDB import SAMDB
x = SAMDB()

from pprint import pprint

result = x.addNewTest('WMS-test', 'wms_test.py', 3600, 3000, 'Check if site is able to execute SAM tests')
pprint(result)
x.addNewTest('CVMFS-test', 'cvmfs_test.py', 3600, 3000, 'Check if CVMFS is correct')
pprint(result)
x.addNewTest('BOSS-test', 'bossexe_test.py&boss.sh', 3600, 3000, 'Check the work of BOSS')
pprint(result)
