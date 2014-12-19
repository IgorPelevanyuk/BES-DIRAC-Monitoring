Ext.define('DIRAC.SAM.classes.SAM', {
    extend : 'Ext.dirac.core.Module',
    requires :['Ext.grid.*',
               'Ext.data.*',
               'Ext.util.*',
               'Ext.state.*'],
    initComponent:function(){
      var me = this;

      me.launcher.title = "CE availability monitoring";
      me.launcher.maximized = false;
    
      me.launcher.width = 650;
      me.launcher.height = 254;
    
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
            url : GLOBAL.BASE_URL + 'SAM/getData',
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
        columns : [{
            header : 'Site',
            sortable : true,
            dataIndex : 'site',
            align : 'left'
        },
        {
            header : 'Test',
            sortable : true,
            dataIndex : 'test',
            align : 'left'
        },
        {
            header : 'Result',
            sortable : true,
            dataIndex : 'result',
            align : 'right',
            renderer : colorerBold
        },
        {
            header : 'Received ago',
            sortable : false,
            dataIndex : 'received',
            align : 'right',
            renderer : secToMin
        },
        {
            header : 'Description',
            sortable : true,
            dataIndex : 'description',
            align : 'right'
        }]
    });

     me.add([me.grid]);
    
    }
});
