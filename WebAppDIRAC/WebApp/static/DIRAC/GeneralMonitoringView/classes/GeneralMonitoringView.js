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
                  {name : 'running', type: 'float'},
                  {name : 'waiting', type: 'float'},
                  {name : 'failed', type: 'float'},
                  {name : 'done', type: 'float'},
                  {name : 'se', type: 'string'},
                  {name : 'sesize', type: 'string'},
                  {name : 'sestatus', type: 'string'}],
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
            renderer: function(val){ return val; }
        },
        {
            header : 'Running',
            sortable : true,
            dataIndex : 'running',
            align : 'right'
        },
        {
            header : 'Waiting',
            sortable : true,
            dataIndex : 'waiting',
            align : 'right'
        },
        {
            header : 'Failed',
            sortable : true,
            dataIndex : 'failed',
            align : 'right'
        },
        {
            header : 'Done',
            sortable : true,
            dataIndex : 'done',
            align : 'right'
        },
        {
            header : 'SE',
            sortable : true,
            dataIndex : 'se',
            align : 'right'
        },
        {
            header : 'SE Ocupied GB',
            sortable : true,
            dataIndex : 'sesize',
            align : 'right'
        },
        {
            header : 'SE status',
            sortable : true,
            dataIndex : 'sestatus',
            align : 'right'
        }]
    });
     me.add([me.grid]);
    
    }
});
