mkdir -p /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB
mkdir -p /opt/dirac/pro/BESDIRAC/FrameworkSystem/Agent/sam_tests
mkdir -p /opt/dirac/pro/BESDIRAC/FrameworkSystem/Service
mkdir -p /opt/dirac/pro/BESDIRAC/FrameworkSystem/Client

cp BESDIRAC/FrameworkSystem/DB/SAMDB.py /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/.
cp BESDIRAC/FrameworkSystem/DB/SAMDB.sql /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/.

cp BESDIRAC/FrameworkSystem/DB/GeneralPurposeDB.py /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/.
cp BESDIRAC/FrameworkSystem/DB/GeneralPurposeDB.sql /opt/dirac/pro/BESDIRAC/FrameworkSystem/DB/.

cp BESDIRAC/FrameworkSystem/Agent/GeneralPurposeAgent.py /opt/dirac/pro/BESDIRAC/FrameworkSystem/Agent/.

cp BESDIRAC/FrameworkSystem/Service/SAMHandler.py /opt/dirac/pro/BESDIRAC/FrameworkSystem/Service/SAMHandler.py
cp BESDIRAC/FrameworkSystem/Client/SAMClient.py /opt/dirac/pro/BESDIRAC/FrameworkSystem/Client/SAMClient.py 

cp BESDIRAC/FrameworkSystem/Agent/SAMLauncherAgent.py /opt/dirac/pro/BESDIRAC/FrameworkSystem/Agent/.

cp sam_tests/* /opt/dirac/pro/BESDIRAC/FrameworkSystem/Agent/sam_tests/.

cp WebAppDIRAC/WebApp/handler/SAMHandler.py /opt/dirac/pro/WebAppDIRAC/WebApp/handler/SAMHandler.py
cp -r WebAppDIRAC/WebApp/static/DIRAC/SAM /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/

cp WebAppDIRAC/WebApp/handler/BusynessMonitorHandler.py /opt/dirac/pro/WebAppDIRAC/WebApp/handler/BusynessMonitorHandler.py
cp -r WebAppDIRAC/WebApp/static/DIRAC/BusynessMonitor  /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/.

cp WebAppDIRAC/WebApp/handler/HostStatHandler.py /opt/dirac/pro/WebAppDIRAC/WebApp/handler/HostStatHandler.py
cp -r WebAppDIRAC/WebApp/static/DIRAC/HostStat /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/

cp WebAppDIRAC/WebApp/handler/SAMChartsHandler.py /opt/dirac/pro/WebAppDIRAC/WebApp/handler/SAMChartsHandler.py
cp -r WebAppDIRAC/WebApp/static/DIRAC/SAMCharts /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/

cp WebAppDIRAC/WebApp/handler/GeneralMonitoringViewHandler.py /opt/dirac/pro/WebAppDIRAC/WebApp/handler/GeneralMonitoringViewHandler.py
cp -r WebAppDIRAC/WebApp/static/DIRAC/GeneralMonitoringView /opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/

echo "Modules deployed"
