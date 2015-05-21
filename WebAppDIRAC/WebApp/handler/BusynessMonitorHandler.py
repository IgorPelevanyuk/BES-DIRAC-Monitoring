from WebAppDIRAC.Lib.WebHandler import WebHandler #@UnresolvedImport
from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB #@UnresolvedImport
from DIRAC.ConfigurationSystem.Client.Config import gConfig  # @UnresolvedImport
from pprint import pprint

class BusynessMonitorHandler(WebHandler):

    AUTH_PROPS = "all"
    
    def web_getData(self):
        siteMaxJobs = {}
        #Calculate Max pledges for Cluster and GRIDs
        for dir in  gConfig.getSections('/Resources/Sites')['Value']:
            for site in gConfig.getSections('/Resources/Sites/'+dir)['Value']:
                if 'CEs' in gConfig.getSections('/Resources/Sites/'+dir+'/'+site)['Value']:
                    for ce in gConfig.getSections('/Resources/Sites/'+dir+'/'+site+'/CEs')['Value']:
                        for queue in gConfig.getSections('/Resources/Sites/'+dir+'/'+site+'/CEs/'+ce+'/Queues')['Value']:
                            siteMaxJobs[site] = siteMaxJobs.get(site, 0) + int(gConfig.getValue('/Resources/Sites/'+dir+'/'+site+'/CEs/'+ce+'/Queues/'+queue+'/MaxTotalJobs'))
        
        #Calculate Max pledges for clouds
        for vm in gConfig.getSections('/Resources/VirtualMachines/CloudEndpoints')['Value']:
            site = gConfig.getValue('/Resources/VirtualMachines/CloudEndpoints/'+vm+'/siteName')
            limit = gConfig.getValue('/Resources/VirtualMachines/CloudEndpoints/'+vm+'/maxEndpointInstances')
            if site is not None and limit is not None:
              siteMaxJobs[site] = int(limit)
        pprint(siteMaxJobs)
        for site in siteMaxJobs:
          siteMaxJobs[site] = {'max': siteMaxJobs[site], 'current':0}
        
        #Get current Running jobs
        import MySQLdb #@UnresolvedImport
        db = MySQLdb.connect(host="diracdb.ihep.ac.cn", # your host, usually localhost
                             user="monitor", # your username
                             passwd="###DIRAC_DB_PASS###", # your password
                             db="JobDB")

        cur = db.cursor()
        cur.execute("select Site, count(*) from Jobs where Status='Running' group by Site")
        for row in cur.fetchall() :
          if row[0] not in siteMaxJobs:
            siteMaxJobs[row[0]] = {'max':0}
          siteMaxJobs[row[0]]['current'] = row[1]

        #Get Weekly Done and Failed jobs
        for site in siteMaxJobs:
          siteMaxJobs[site]['week_done'] = 0
          siteMaxJobs[site]['week_failed'] = 0
        cur.execute("select Site, count(*), min(SubmissionTime), max(SubmissionTime) from Jobs where (Status='Done') and SubmissionTime>DATE_SUB(NOW(), INTERVAL 168 HOUR) group by Site")
        for row in cur.fetchall():
          if row[0] not in siteMaxJobs:
            siteMaxJobs[row[0]] = {'max':0, 'current':0, 'week_done':0, 'week_failed':0}
          siteMaxJobs[row[0]]['week_done'] = row[1]

        cur.execute("select Site, count(*), min(SubmissionTime), max(SubmissionTime) from Jobs where (Status='Failed') and SubmissionTime>DATE_SUB(NOW(), INTERVAL 168 HOUR) group by Site")
        for row in cur.fetchall():
          if row[0] not in siteMaxJobs:
            siteMaxJobs[row[0]] = {'max':0, 'current':0, 'week_done':0, 'week_failed':0}
          siteMaxJobs[row[0]]['week_failed'] = row[1]
        cur.close()

        res = []
        for site in siteMaxJobs:
          res.append({'site':site, 'max':siteMaxJobs[site]['max'], 'current':siteMaxJobs[site]['current'], 'week_done':siteMaxJobs[site]['week_done'], 'week_failed':siteMaxJobs[site]['week_failed']})
        #from DIRAC.WorkloadManagementSystem.DB.JobDB import JobDB
        #db = JobDB()
        #cmd = 'SELECT count(*) FROM Jobs'
        #res = db._query( cmd )
        #print res 
        print siteMaxJobs

        self.write({"result":res})


