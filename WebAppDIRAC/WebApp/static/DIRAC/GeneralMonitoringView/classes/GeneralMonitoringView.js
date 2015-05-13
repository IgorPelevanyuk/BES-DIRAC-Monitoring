Ext.define('DIRAC.GeneralMonitoringView.classes.GeneralMonitoringView', {
    extend : 'Ext.dirac.core.Module',
    requires :['Ext.grid.*',
               'Ext.data.*',
               'Ext.util.*',
               'Ext.state.*',
               'Ext.date.*'],
    initComponent:function(){
      var me = this;

      me.launcher.title = "GRID Overview";
      me.launcher.maximized = false;
    
      me.launcher.width = 1000;
      me.launcher.height = 500;
    
      me.launcher.x = 0;
      me.launcher.y = 0;
    
      Ext.apply(me, {
        layout : 'border',
        bodyBorder : false,
        defaults : {
          collapsible : true,
          split : true
        }
      });
    
      me.callParent(arguments);
    },

    buildUI:function(){

      function colorerBold(val) {
        if (val == 'Success') {
            return '<span style="color:green;"><b>' + val + '</b></span>';
        }
        if (val == 'Banned')
            return '<span style="color:gray;"><b>Banned</b></span>';
        if (val == 'Timeout')
            return '<span style="color:black;"><b>Timeout</b></span>';
        if (val == 'Fail')
            return '<span style="color:red;"><b>Fail</b></span>';
        return val
      }
      function colorer(val) {
        if (val == 'Success') {
            return '<span style="color:green;">' + val + '</span>';
        } else if (val =='runned_failed') {
            return '<span style="color:red;">Fail</span>';
        }
        return val;
      }

      function gradientR(num) {
        if (num<=0.5)
          var res=255;
        else 
          var res = (255-2*(num-0.5)*255);
        return parseInt(res).toString();
      }
      function gradientG(num) {
        if (num>=0.5)
          var res=255;
        else 
          var res = 2*(num*255);
        return parseInt(res).toString();
      } 
      function rateColorer(val) {
        return '<span style="background:rgb('+gradientR(val)+','+gradientG(val)+',0);">'+val.toFixed(2)+'</span>';
      }
      function secToMin(val) {
        return (Math.floor(val/60)).toString() + ' min';
      }
      var me = this;

      me.dataStore = new Ext.data.JsonStore({

        proxy : {
            type : 'ajax',
            url : GLOBAL.BASE_URL + 'GeneralMonitoringView/getData',
            reader : {
                type : 'json',
                root : 'result'
            },
            timeout : 50000
        },
        fields : [{name : 'site', type : 'string' },
                  {name : 'test', type: 'string'},
                  {name : 'result', type: 'string'},
                  {name : 'received', type: 'float'},
                  {name : 'description', type: 'string'}],
        autoLoad : true,
        pageSize : 20,

    });

      me.grid = Ext.create('Ext.grid.Panel', {
        region : 'center',
        store : me.dataStore,
        header : false,
        listeners: {
            itemclick: function(dv, record, item, index, e) {
                console.log(record.get('site')+ ':' +record.get('test'));
                view_showHistory(record.get('site'), record.get('test'));
            }
        },
        columns : [{
            header : 'Site',
            sortable : true,
            dataIndex : 'site',
            align : 'left',
            renderer: function(val){ return val; },
        },
        {
            header : 'Tests',
            sortable : true,
            dataIndex : 'testStatus',
            align : 'left'
        },
        {
            header : 'Hosts',
            sortable : true,
            dataIndex : 'hostStatus',
            align : 'right',
            renderer : colorerBold
        },
        {
            header : 'Running jobs',
            sortable : false,
            dataIndex : 'jobsRunning',
            align : 'right',
            renderer : secToMin
        },
        {
            header : 'Scheduled jobs',
            sortable : true,
            dataIndex : 'jobScheduled',
            align : 'right'
        },
        {
            header : 'Failed jobs',
            sortable : true,
            dataIndex : 'jobsFailed',
            align : 'right'
        },
        {
            header : 'Finished jobs',
            sortable : true,
            dataIndex : 'jobFinished',
            align : 'right'
        }]
    });
     me.add([me.grid]);
    
    }
});
