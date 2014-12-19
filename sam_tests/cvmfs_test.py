# Replace standart service URL with vm162 service URL
import DIRAC.Core.DISET.RPCClient as A
import DIRAC.Core.DISET.private.BaseClient as B
def foo(serviceName, serviceTuple = False, setup = False ):
    print 'Hey'
    return 'dips://vm162.jinr.ru:2170/Framework/SAM'

B.getServiceURL = foo
RPC = A.RPCClient("Framework/SAM")
import socket
hostname = socket.gethostname()
#------------------------------------------------------------------------------
CVMFS_DIR = '/cvmfs/boss.cern.ch/'

# Check correctness of log [ ['anyMgr','INFO ...'], ['anyMgr2','SUCCESS ...'], ...]
def isCorrect(output, errors):
    if len(errors) == 0:
        return True
    return False

#Built bash command and execute it
import subprocess
popen = subprocess.Popen(["ls", CVMFS_DIR], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = popen.communicate()
output = result[0]
errors = result[1]

print "We successfully sent the test to the server. The output is:"
print output
print "====================================================================================="
print "The error message is:"
print errors
print "====================================================================================="
print "Check correctness:"



import sys
if isCorrect(output, errors):
    result = RPC.setResult('Success', int(sys.argv[1]), 'Success', hostname)
else:
    result = RPC.setResult('Fail', int(sys.argv[1]), CVMFS_DIR + ' not found' , hostname)
print result

