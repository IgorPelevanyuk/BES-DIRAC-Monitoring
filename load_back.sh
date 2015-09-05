cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/SAMDB.py BESDIRAC/FrameworkSystem/DB/SAMDB.py
cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/SAMDB.sql BESDIRAC/FrameworkSystem/DB/SAMDB.sql

cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/GeneralPurposeDB.py BESDIRAC/FrameworkSystem/DB/GeneralPurposeDB.py
cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/GeneralPurposeDB.sql BESDIRAC/FrameworkSystem/DB/GeneralPurposeDB.sql

cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/Agent/GeneralPurposeAgent.py BESDIRAC/FrameworkSystem/Agent/GeneralPurposeAgent.py

cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/Agent/sam_tests/* sam_tests/.

cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/Service/SAMHandler.py BESDIRAC/FrameworkSystem/Service/SAMHandler.py
cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/Client/SAMClient.py BESDIRAC/FrameworkSystem/Client/SAMClient.py

cp /opt/dirac/pro/BESDIRAC/FrameworkSystem/Agent/SAMLauncherAgent.py BESDIRAC/FrameworkSystem/Agent/SAMLauncherAgent.py

cp /opt/dirac/pro/WebAppDIRAC/WebApp/handler/SAMHandler.py WebAppDIRAC/WebApp/handler/SAMHandler.py
cp -r /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/SAM WebAppDIRAC/WebApp/static/DIRAC/

#cp /opt/dirac/pro/WebAppDIRAC/WebApp/handler/BusynessMonitorHandler.py WebAppDIRAC/WebApp/handler/BusynessMonitorHandler.py
cp -r /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/BusynessMonitor WebAppDIRAC/WebApp/static/DIRAC/

#cp /opt/dirac/pro/WebAppDIRAC/WebApp/handler/HostStatHandler.py WebAppDIRAC/WebApp/handler/HostStatHandler.py
cp -r /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/HostStat WebAppDIRAC/WebApp/static/DIRAC/

cp /opt/dirac/pro/WebAppDIRAC/WebApp/handler/SAMChartsHandler.py WebAppDIRAC/WebApp/handler/SAMChartsHandler.py
cp -r /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/SAMCharts WebAppDIRAC/WebApp/static/DIRAC/

#cp /opt/dirac/pro/WebAppDIRAC/WebApp/handler/GeneralMonitoringViewHandler.py WebAppDIRAC/WebApp/handler/GeneralMonitoringViewHandler.py
cp -r /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/GeneralMonitoringView WebAppDIRAC/WebApp/static/DIRAC/
