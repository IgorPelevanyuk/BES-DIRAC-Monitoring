Ext.define('DIRAC.SAM.classes.SAM', {
    extend: 'Ext.dirac.core.Module',
    requires: [ 'Ext.grid.*',
              'Ext.data.*',
              'Ext.util.*',
              'Ext.state.*',
              'Ext.date.*' ],
    initComponent: function() {
        var me = this;
        me.launcher.title = "CE availability monitoring";
        me.launcher.maximized = false;
        me.launcher.width = 650;
        me.launcher.height = 254;
        me.launcher.x = 0;
        me.launcher.y = 0;
        Ext.apply(me, {
            layout: 'border',
            bodyBorder: false,
            defaults: {
                collapsible: true,
                split: true
            }
        });
        me.callParent(arguments);
    },

    buildUI: function() {
    function view_showHistory(site, test) {

      var data_store = new Ext.data.JsonStore({
        proxy: {
          type: 'ajax',
          url: GLOBAL.BASE_URL + 'SAM/getSiteMonthAvailability?site=' + site + '&test=' + test,
          method: 'GET',
          reader: { 
              type: 'json',
              root: 'result'
          },
          timeout: 50000
        },
        fields: [ { name: 'time', type: 'date', dateFormat: 'Y-m-d H:i:s' },
                  { name: 'state', type: 'integer' },
                  { name: 'description', type: 'string' } ],
        autoLoad: true,
        pageSize: 20,
      });
       
      var state_map = { 1:'Banned', 2:'Fail', 4:'Timeout', 5:'Success' };
      var chart = Ext.create('Ext.chart.Chart', {
                  width: 500,
                  height: 300,
                  animate: true,
                  shadow: false,
                  store: data_store,
                  axes: [ {
                      type: 'Numeric',
                      position: 'left',
                      fields: [ 'state' ],
                      label: {
                          renderer: function(state_num) {
                              if (state_num in state_map)
                                  return state_map[state_num];
                              return "";
                          }
                      },
                      title: 'Test Result',
                      grid: true,
                      minimum: 0
                  }, {
                      type: 'Time',
                      dateFormat: 'd M H:i',
                      position: 'bottom',
                      fields: [ 'time' ],
                      title: 'Time',
                      grid: true,
                      label: {
                          rotate: {
                              degrees: -44
                          }
                      }
                  } ],
                  series: [ {
                      type: 'scatter',
                      markerCfg: {
                          radius: 5,
                          size: 5
                      },
                      axis: 'bottom',                        
                      highlight: true,
                      tips: {
                          trackMouse: true,
                          width: 200,
                          height: 40,
                          renderer: function(storeItem, item) {
                              var time = Ext.Date.format(storeItem.get('time'), 'd M Y H:i');
                              var state_map = { 1:'Banned', 2:'Fail', 4:'Timeout', 5:'Success' };
                              var state = '';
                              if (storeItem.get('state') in state_map)
                                  state = state_map[storeItem.get('state')];
                              else
                                  state = 'Undefined' + storeItem.get('state').toString() + '<br>' + storeItem.get('description');
                              this.setTitle(time + ': ' + state + '. ' + '<br>' + storeItem.get('description'));
                          }
                      }, 
                      xField: 'time',
                      yField: [ 'state' ],
                      renderer: function(sprite, record, attr, index, store) {
                          var value = record.get('state');
                          var color = [ 'rgb(213, 70, 121)', 'rgb(0, 0, 0)', 'rgb(200, 6, 40)', 'rgb(49, 149, 0)', 'rgb(100, 100, 100)', 'rgb(49, 149, 0)' ][value];
                          return Ext.apply(attr, {
                              fill: color,
                              size: 3,
                              radius:3
                          });
                      }
                  }, {
                      type: 'line',
                      xField: 'time',
                      yField: 'state',
                      showMarkers: false
                  } ]
              });

      var win = Ext.create('Ext.Window', {
           width: 800,
           height: 600,
           hidden: false,
           maximizable: true,
           title: site + ' ' + test,
           renderTo: Ext.getBody(),
           layout: 'fit',
           tbar: [ {
               text: 'Reload',
               handler: function() {
                   console.log('Button pressed');
               }
           } ],
           items: [ chart ]
      });
      Ext.WindowManager.register(win);
      Ext.WindowManager.bringToFront(win);
    }

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
      return val;
    }

    function secToMin(val) {
      return (Math.floor(val / 60)).toString() + ' min';
    }
    var me = this;

    me.dataStore = new Ext.data.JsonStore({

      proxy: {
          type: 'ajax',
          url: GLOBAL.BASE_URL + 'SAM/getData',
          reader: {
              type: 'json',
              root: 'result'
          },
          timeout: 50000
      },
      fields: [ { name: 'site', type: 'string' },
                { name: 'test', type: 'string' },
                { name: 'result', type: 'string' },
                { name: 'received', type: 'float' },
                { name: 'description', type: 'string' } ],
      autoLoad: true,
      pageSize: 20,

    });

    me.grid = Ext.create('Ext.grid.Panel', {
      region: 'center',
      store: me.dataStore,
      header: false, 
      listeners: {
          itemclick: function(dv, record, item, index, e) {
              console.log(record.get('site') + ':' +record.get('test'));
              view_showHistory(record.get('site'), record.get('test'));
          }
      },
      columns: [ {
          header: 'Site',
          sortable: true,
          dataIndex: 'site',
          align: 'left',
          renderer: function(val) { return val; },
      },
      {
          header: 'Test',
          sortable: true,
          dataIndex: 'test',
          align: 'left'
      },
      {
          header: 'Result',
          sortable: true,
          dataIndex: 'result',
          align: 'right',
          renderer: colorerBold
      },
      {
          header: 'Received ago',
          sortable: false,
          dataIndex: 'received',
          align: 'right',
          renderer: secToMin
      },
      {
          header: 'Description',
          sortable: true,
          dataIndex: 'description',
          align: 'right'
      } ]
    });
    me.add([ me.grid ]);

    }
});
