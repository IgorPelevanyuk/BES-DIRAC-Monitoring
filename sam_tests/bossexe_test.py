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


# Check correctness of log [ ['anyMgr','INFO ...'], ['anyMgr2','SUCCESS ...'], ...]
def isCorrect(logs):
    applicationMgrSuccess = 0
    dstHltMakerSuccess = 0
    expectedApplicationMng = 'INFO Application Manager Terminated successfully' 
    expectedDstHltMaker = 'SUCCESS 50 events are converted.'
    for i in logs:
        if i[0]=='ApplicationMgr' and i[1]==expectedApplicationMng:
            applicationMgrSuccess += 1
        if i[0]=='DstHltMaker' and i[1]==expectedDstHltMaker:
            dstHltMakerSuccess += 1
    if applicationMgrSuccess==2 and dstHltMakerSuccess==1:
        return True 
    return False

def whyError(output, errors):
    if "boss.exe: command not found" in errors:
        return "boss.exe not found"
    return "Error unclear"

#Built bash command and execute it
import subprocess
popen = subprocess.Popen(["bash", "boss.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

lines = output.split('\n')
for i in range(0, len(lines)):
    lines[i] = lines[i].split(' ',1)
toKeep = ['DstHltMaker', 'ApplicationMgr']
dry = [i for i in lines if i[0] in toKeep]
for i in dry:
    i[1]=i[1].strip()




import sys
if isCorrect(dry):
    result = RPC.setResult('Success', int(sys.argv[1]), 'Success', hostname)
else:
    result = RPC.setResult('Fail', int(sys.argv[1]), whyError(output, errors), hostname)
print result

