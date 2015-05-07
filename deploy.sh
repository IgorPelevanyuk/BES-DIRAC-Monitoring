cp DIRAC/FrameworkSystem/DB/SAMDB.py /opt/dirac/pro/DIRAC/FrameworkSystem/DB/.
cp DIRAC/FrameworkSystem/DB/SAMDB.sql /opt/dirac/pro/DIRAC/FrameworkSystem/DB/.

cp DIRAC/FrameworkSystem/Service/SAMHandler.py /opt/dirac/pro/DIRAC/FrameworkSystem/Service/SAMHandler.py
cp DIRAC/FrameworkSystem/Client/SAMClient.py /opt/dirac/pro/DIRAC/FrameworkSystem/Client/SAMClient.py 

cp DIRAC/FrameworkSystem/Agent/SAMLauncherAgent.py /opt/dirac/pro/DIRAC/FrameworkSystem/Agent/.

cp sam_tests/* /opt/dirac/pro/DIRAC/FrameworkSystem/Agent/sam_tests/.

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
