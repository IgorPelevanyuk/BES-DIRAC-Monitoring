Ext.define('DIRAC.SAMCharts.classes.SAMCharts', {
    extend : 'Ext.dirac.core.Module',
    requires :['Ext.chart.*',
               'Ext.Window',
               'Ext.data.*',
               'Ext.fx.target.Sprite',
               'Ext.layout.container.Fit'],

    initComponent:function(){
      var me = this;

      me.launcher.title = "CE charts monitoring";
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
     var me = this;
     window.store1 = Ext.create('Ext.data.JsonStore', {
        fields: ['name', 'data1'],
        data: [{name:'x', data1:10}, {name:'y', data1:20}]
     });
     
     me.dataStore = new Ext.data.JsonStore({
        proxy : {
            type : 'ajax',
            //url : GLOBAL.BASE_URL + 'SAMCECharts/getSiteChartData?site=BES.JINR.RU',
            url : GLOBAL.BASE_URL + 'SAMCharts/getSiteMonthAvailability?site=GRID.JINR.RU',

            method : 'GET',
            params : {site:'GRID.JINR.ru'},
            reader : {
                type : 'json',
                root : 'result'
            },
            timeout : 50000
        },
        fields : [{name : 'time', type : 'string' },
                  {name : 'test', type : 'integer'},
                  {name : 'state', type: 'string' }],
        autoLoad : true,
        pageSize : 20,

    });
    
     var win = Ext.create('Ext.Window', {
        width: 800,
        height: 600,
        hidden: false,
        maximizable: true,
        title: 'Site availability',
        renderTo: Ext.getBody(),
        layout: 'fit',
        tbar: [{
            text: 'Reload Data',
            handler: function() {
                store1.loadData(generateData(8));
            }
        }],
        items: [{
            html : "<div id='" + me.id + "-statistics-plot' style='width:100%;'></div>",
            xtype : "box",
            cls : 'jm-statistics-plot-background'
       }]
    });
    }    
});
