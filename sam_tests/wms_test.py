import DIRAC.Core.DISET.RPCClient as A
B = A.InnerRPCClient
import DIRAC.Core.DISET.private.BaseClient as C
def foo(serviceName, serviceTuple = False, setup = False ):
    print 'Hey'
    return 'dips://badger01.ihep.ac.cn:9280/Framework/SAM'

C.getServiceURL = foo
x = A.RPCClient("Framework/SAM")
import socket
hostname = socket.gethostname()


import sys
result = x.setResult('Success', int(sys.argv[1]), 'Remote call', hostname)
print result

