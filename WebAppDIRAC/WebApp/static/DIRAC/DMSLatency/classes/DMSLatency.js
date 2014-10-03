Ext.define('DIRAC.DMSLatency.classes.DMSLatency', {
    extend : 'Ext.dirac.core.Module',
    requires :['Ext.grid.*',
               'Ext.data.*',
               'Ext.util.*',
               'Ext.state.*'],
    initComponent:function(){
      var me = this;

      me.launcher.title = "SE latency monitoring";
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
      function failer(val) {
        if (val == -1) {
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
            url : GLOBAL.BASE_URL + 'DMSLatency/getData',
            reader : {
                type : 'json',
                root : 'result'
            },
            timeout : 50000
        },
        fields : [{name : 'site', type : 'string' },
                  {name : 'destination', type: 'string'},
                  {name : 'latency', type: 'float'}],
        autoLoad : true,
        pageSize : 20,

    });

      me.grid = Ext.create('Ext.grid.Panel', {
        region : 'center',
        store : me.dataStore,
        header : false,
        columns : [{
            header : 'Source',
            sortable : true,
            dataIndex : 'site',
            align : 'left'
        },
        {
            header : 'Destination',
            sortable : true,
            dataIndex : 'destination',
            align : 'left'
        },
        {
            header : 'Latency(sec)',
            sortable : true,
            dataIndex : 'latency',
            align : 'right',
            renderer : failer
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
