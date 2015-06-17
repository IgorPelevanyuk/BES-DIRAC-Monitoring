Ext.define('DIRAC.GeneralMonitoringView.classes.GeneralMonitoringView', {
    extend: 'Ext.dirac.core.Module',
    requires: ['Ext.grid.*',
        'Ext.data.*',
        'Ext.util.*',
        'Ext.state.*',
        'Ext.date.*'
    ],
    initComponent: function () {
        var me = this;
        me.launcher.title = "GRID Overview";
        me.launcher.maximized = false;
        me.launcher.width = 1000;
        me.launcher.height = 500;
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
    buildUI: function () {
        var me = this;

        function sestatusRenderer(value, meta, record, row, col) {
            if (value === "")
                return '';
            if (value != 'Fail') {
                meta.style = "background-color:green;";
            } else {
                meta.style = "background-color:red;";
            }
            var description = me.dataStore.getRange()[row].data.sedescription;
            meta.tdAttr = 'data-qtip="' + description + '"';
            return value;
        }

        function runningVSwaitingRenderer(value, meta, record) {
            if (((record.data.waiting !== 0) && (record.data.running === 0)) || (1.0 * record.data.waiting / record.data.running > 2)) {
                meta.style = "background-color:red;";
            }
            return value.toString();
        }
        me.dataStore = new Ext.data.JsonStore({
            proxy: {
                type: 'ajax',
                url: GLOBAL.BASE_URL + 'GeneralMonitoringView/getData',
                reader: {
                    type: 'json',
                    root: 'result'
                },
                timeout: 50000
            },
            fields : [{name : 'site', type : 'string' },
                      {name : 'running', type: 'float'},
                      {name : 'waiting', type: 'float'},
                      {name : 'failed', type: 'float'},
                      {name : 'done', type: 'float'},
                      {name : 'se', type: 'string'},
                      {name : 'sesize', type: 'string'},
                      {name : 'sestatus', type: 'string'},
                      {name : 'sedescription', type: 'string'}],
            autoLoad: true,
            pageSize: 20,
        });
        me.grid = Ext.create('Ext.grid.Panel', {
            region: 'center',
            store: me.dataStore,
            header: false,
            columns: [{
                header: 'Site',
                sortable: true,
                dataIndex: 'site',
                align: 'left',
            }, {
                header: 'Running',
                sortable: true,
                dataIndex: 'running',
                align: 'right',
                renderer: runningVSwaitingRenderer
            }, {
                header: 'Waiting',
                sortable: true,
                dataIndex: 'waiting',
                align: 'right',
                renderer: runningVSwaitingRenderer
            }, {
                header: 'Failed',
                sortable: true,
                dataIndex: 'failed',
                align: 'right'
            }, {
                header: 'Done',
                sortable: true,
                dataIndex: 'done',
                align: 'right'
            }, {
                header: 'SE',
                sortable: true,
                dataIndex: 'se',
                align: 'right'
            }, {
                header: 'SE Ocupied GB',
                sortable: true,
                dataIndex: 'sesize',
                align: 'right'
            }, {
                header: 'SE status',
                sortable: true,
                dataIndex: 'sestatus',
                align: 'right',
                renderer: sestatusRenderer
            }]
        });
        me.add([me.grid]);
    }
});