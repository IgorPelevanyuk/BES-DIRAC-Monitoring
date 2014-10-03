Ext.define('DIRAC.NetStat.classes.NetStat', {
    extend : 'Ext.dirac.core.Module',
    requires :['Ext.grid.*',
               'Ext.data.*',
               'Ext.util.*',
               'Ext.state.*'],
    initComponent:function(){
      var me = this;

      me.launcher.title = "Network monitoring";
      me.launcher.maximized = false;
    
      me.launcher.width = 650;
      me.launcher.height = 650;
    
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
        } else {
            return '<span style="color:red;"><b>Fail</b></span>';
        }
        return val;
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
      var me = this;

      me.dataStore = new Ext.data.JsonStore({

        proxy : {
            type : 'ajax',
            url : GLOBAL.BASE_URL + 'NetStat/getData',
            reader : {
                type : 'json',
                root : 'result'
            },
            timeout : 50000
        },
        fields : [{name : 'site', type : 'string' },
                  {name : 'host', type: 'string'},
                  {name : 'cetype', type: 'string'},
                  {name : 'avgping', type: 'float'},
                  {name : 'passed', type: 'float'},
                  {name : 'description', type: 'string'}],
        autoLoad : true,
        pageSize : 20,

    });

      me.grid = Ext.create('Ext.grid.Panel', {
        region : 'center',
        store : me.dataStore,
        header : false,
        columns : [{
            header : 'Site',
            sortable : true,
            dataIndex : 'site',
            align : 'left'
        },
        {
            header : 'Host',
            sortable : true,
            dataIndex : 'host',
            align : 'left'
        },
        {
            header : 'CEType',
            sortable : true,
            dataIndex : 'cetype',
            align : 'left'
        },
        {
            header : 'AverageTime',
            sortable : true,
            dataIndex : 'avgping',
            align : 'right'
        },
        {
            header : 'Passed',
            sortable : true,
            dataIndex : 'passed',
            align : 'right',
            renderer : rateColorer
        },
	{
            header : 'Description',
            sortable : true,
            dataIndex : 'description',
            align : 'left'
        }]
        //{
        //    header : 'OldStatus',
        //    sortable : true,
        //    dataIndex : 'old_status',
        //    align : 'right',
        //    renderer : colorer
        //}]
        
    });

     me.add([me.grid]);
    
    }
});
