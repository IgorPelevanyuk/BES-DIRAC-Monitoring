from WebAppDIRAC.Lib.WebHandler import WebHandler #@UnresolvedImport
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB #@UnresolvedImport

import math

USE_PURE_MYSQL = True


def trunc(f):
    '''Truncates/pads a float f to n decimal places without rounding'''
    temp = f*100
    temp = math.floor(temp)
    temp = temp/100
    return temp


def choose(condition, satisfy, unsatisfy):
    if condition:
      return satisfy
    else:
      return unsatisfy

def mysql_querry(querry):
    if USE_PURE_MYSQL:
        import MySQLdb#@UnresolvedImport
        db = MySQLdb.connect(host="diracdb2.ihep.ac.cn", # your host, usually localhost
                         user="monitor", # your username
                         passwd="###DIRAC_DB_PASS###", # your password
                         db="JobDB")
        cur = db.cursor()
        cur.execute(querry)
        data = cur.fetchall()
        cur.close()
        return data
    else:
        db = JobDB()
        return db._query( querry )['Value']


class HostStatHandler(WebHandler): 

    AUTH_PROPS = "all"

    def getDataFromDB(self):
           db = JobDB()
           cmd = 'SELECT * FROM Jobs'
           res = db._query( cmd ) 

           #Week data
           cmd = "select J.Site, JP.Value, sum(1),  S.total from Jobs J, JobParameters JP, (select JP.Value as host, sum(1) as total from Jobs J, JobParameters JP where J.JobID=JP.JobID and JP.Name='HostName' group by JP.Value) S where J.JobID=JP.JobID and JP.Name='HostName' and J.Status='Done' and S.host=JP.Value group by JP.Value order by J.Site asc"

           result = mysql_querry( cmd )
           #print result
           data = {}
           for i in result:
             data[(i[0], i[1])]=[int(i[2]), int(i[3])]

           #TwoDays data
           cmd = "select J.Site, JP.Value, sum(1), S.total from Jobs J, JobParameters JP, (select JP.Value as host, sum(1) as total from Jobs J, JobParameters JP where J.JobID=JP.JobID and JP.Name='HostName' and J.SubmissionTime>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 48 HOUR) group by JP.Value) S where J.JobID=JP.JobID and JP.Name='HostName' and J.Status='Done' and S.host=JP.Value and J.SubmissionTime>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 48 HOUR) group by JP.Value order by J.Site asc"

           result = mysql_querry( cmd )
           for i in result:
             if (i[0],i[1]) not in data:
                data[(i[0],i[1])] = [0,0]
                print "Strange behavior: for ", (i[0],i[1]), " was no week data"
             data[(i[0], i[1])] += [int(i[2]), int(i[3])]


           #OneDay data
           cmd = "select J.Site, JP.Value, sum(1),  S.total from Jobs J, JobParameters JP, (select JP.Value as host, sum(1) as total from Jobs J, JobParameters JP where J.JobID=JP.JobID and JP.Name='HostName' and J.SubmissionTime>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 24 HOUR) group by JP.Value) S where J.JobID=JP.JobID and JP.Name='HostName' and J.Status='Done' and S.host=JP.Value and J.SubmissionTime>= DATE_SUB(UTC_TIMESTAMP(),INTERVAL 24 HOUR) group by JP.Value order by J.Site asc"

           result = mysql_querry( cmd )
           for i in result:
             if (i[0],i[1]) not in data:
                data[(i[0],i[1])] = [0,0]
                print "Strange behavior: for ", (i[0],i[1]), " was no week data"
             data[(i[0], i[1])] += [int(i[2]), int(i[3])]

           prejson = [[x[0], x[1]]+data[x] for x in data]
           for i in range(0, len(prejson)):
             prejson[i] += [0 for j in range(0, 8-len(prejson[i]))] 

           return prejson


    def web_getData(self):
            states = self.getDataFromDB()
            print 'INFO ', len(states), ' states had been retrieved'
            result=[]
            for st in states:
                temp = {}
                temp['site'] = st[0]
                temp['host'] = st[1]
                temp['successes'] = choose(st[2]!=0, st[2], 0)
                temp['total'] = choose(st[3]!=0, st[3], 0)
                temp['fails'] = int(st[3]) - int(st[2])
                if int(st[3])!=0:
                    temp['rate'] = trunc(int(st[2])*1.0/int(st[3]))
                else:
                    temp['rate'] = 0

                temp['successes48'] = int(st[4])
                temp['total48'] = int(st[5])
                temp['fails48'] = int(st[5]) - int(st[4])
                if int(st[5])!=0:
                    temp['rate48'] = trunc(int(st[4])*1.0/int(st[5]))
                else:
                    temp['rate48'] = 0

                temp['successes24'] = int(st[6])
                temp['total24'    ] = int(st[7])
                temp['fails24'] = int(st[7]) - int(st[6])
                if int(st[7])!=0:
                    temp['rate24'] = trunc(int(st[6])*1.0/int(st[7]))
                else:
                    temp['rate24'] = 0
                result.append(temp)
            from pprint import pprint
            #pprint(result)
            self.write({"result":result})

