Ext.define('DIRAC.HostStat.classes.HostStat', {
    extend : 'Ext.dirac.core.Module',
    requires :['Ext.grid.*',
               'Ext.data.*',
               'Ext.util.*',
               'Ext.state.*'],
    initComponent:function(){
      var me = this;

      me.launcher.title = "Host monitoring";
      me.launcher.maximized = false;
    
      me.launcher.width = 680;
      me.launcher.height = 600;
    
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
        console.log('RATE_COLORER');
        if (val !=0)
          return '<span style="background:rgb('+gradientR(val)+','+gradientG(val)+',0);">'+val.toFixed(2)+'</span>';
        else
          return "";
      }

      function zeroRemover(val) {
        if (val == 0)
          return "";
        else return val.toString();
      }
     
      function zeroBoldRemover(val) {
        if (val == 0)
          return "";
        else return "<b>"+val.toString()+"</b>";
      }
      var me = this;

      me.dataStore = new Ext.data.JsonStore({

        proxy : {
            type : 'ajax',
            url : GLOBAL.BASE_URL + 'HostStat/getData',
            reader : {
                type : 'json',
                root : 'result'
            },
            timeout : 100000
        },
        fields : [{name : 'site', type : 'string' },
                  {name : 'host', type: 'string'},
                  {name : 'successes24', type: 'int'},
                  {name : 'total24', type: 'int'},
                  {name : 'fails24', type: 'int'},
                  {name : 'rate24', type: 'float'},
                  {name : 'successes48', type: 'int'},
                  {name : 'total48', type: 'int'},
                  {name : 'fails48', type: 'int'},
                  {name : 'rate48', type: 'float'},
                  {name : 'successes', type: 'int'},
                  {name : 'total', type: 'int'},
                  {name : 'fails', type: 'int'},
                  {name : 'rate', type: 'float'}],
        autoLoad : true,
        pageSize : 20,

    });
      var WIDTH_S = 50;
      var WIDTH_M = 70;
      var WIDTH_XL = 200;
      console.log('TOUCH')
      me.grid = Ext.create('Ext.grid.Panel', {
        region : 'center',
        store : me.dataStore,
        features: [{
            ftype: 'summary'
        }],
        header : false,
        columns : [{
            header : 'Site',
            sortable : true,
            dataIndex : 'site',
            align : 'left',
        },
        {
            header : 'Host',
            sortable : true,
            dataIndex : 'host',
            align : 'left',
            width: WIDTH_XL
        },
        {
            header : '24H Successes',
            sortable : true,
            dataIndex : 'successes24',
            align : 'right',
            width: WIDTH_S,
            renderer: zeroRemover,
            summaryType: 'sum'
        },
        {
            header : '24H Total',
            sortable : true,
            dataIndex : 'total24',
            align : 'right',
            width: WIDTH_S,
            renderer: zeroRemover,
            summaryType: 'sum'
        },
        {
            header : '24H Fails',
            sortable : true,
            dataIndex : 'fails24',
            align : 'right',
            width: WIDTH_S,
            renderer: zeroBoldRemover,
            summaryType: 'sum'
        },
        {
            header : '24H Rate',
            sortable : true,
            dataIndex : 'rate24',
            align : 'right',
            width: WIDTH_M,
            renderer : rateColorer
        },
        {  
            header : '48H Successes',
            sortable : true,
            dataIndex : 'successes48',
            align : 'right',
            width: WIDTH_S,
            renderer: zeroRemover,
            summaryType: 'sum'
        },
        {  
            header : '48H Total',
            sortable : true,
            dataIndex : 'total48',
            align : 'right',
            width: WIDTH_S,
            renderer: zeroRemover,
            summaryType: 'sum'
        },
        {  
            header : '48H Fails',
            sortable : true,
            dataIndex : 'fails48',
            align : 'right',
            width: WIDTH_S,
            renderer: zeroBoldRemover,
            summaryType: 'sum'
        },
        {
            header : '48H Rate',
            sortable : true,
            dataIndex : 'rate48',
            align : 'right',
            width: WIDTH_M,
            renderer : rateColorer
        },
        {  
            header : 'Week Successes',
            sortable : true,
            dataIndex : 'successes',
            align : 'right',
            width: WIDTH_S,
            summaryType: 'sum'
        },
        {  
            header : 'Week Total',
            sortable : true,
            dataIndex : 'total',
            align : 'right',
            width: WIDTH_S,
            summaryType: 'sum'
        },
        {  
            header : 'Week Fails',
            sortable : true,
            dataIndex : 'fails',
            align : 'right',
            width: WIDTH_S,
            renderer: zeroBoldRemover,
            summaryType: 'sum'
        },
        {  
            header : 'Week Rate',
            sortable : true,
            dataIndex : 'rate',
            align : 'right',
            width: WIDTH_M,
            renderer : rateColorer
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
