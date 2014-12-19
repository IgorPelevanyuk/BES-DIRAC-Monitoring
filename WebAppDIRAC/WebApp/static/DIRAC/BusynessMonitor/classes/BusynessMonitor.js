Ext.define('DIRAC.BusynessMonitor.classes.BusynessMonitor', {
    extend: 'Ext.dirac.core.Module',
    requires: ['Ext.grid.*',
        'Ext.data.*',
        'Ext.util.*',
        'Ext.state.*'
    ],
    initComponent: function() {
        var me = this;

        me.launcher.title = "Busyness monitoring";
        me.launcher.maximized = false;

        me.launcher.width = 680;
        me.launcher.height = 600;

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
            } else if (val == 'runned_failed') {
                return '<span style="color:red;">Fail</span>';
            }
            return val;
        }

        function gradientR(num) {
            if (num <= 0.5)
                var res = 255;
            else
                var res = (255 - 2 * (num - 0.5) * 255);
            return parseInt(res).toString();
        }

        function gradientG(num) {
            if (num >= 0.5)
                var res = 255;
            else
                var res = 2 * (num * 255);
            return parseInt(res).toString();
        }

        function rateColorer(val) {
            if (val != 0)
                return '<span style="background:rgb(' + gradientR(val) + ',' + gradientG(val) + ',0);">' + val.toFixed(2) + '</span>';
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
            else return "<b>" + val.toString() + "</b>";
        }
        var me = this;

        me.dataStore = new Ext.data.JsonStore({

            proxy: {
                type: 'ajax',
                url: GLOBAL.BASE_URL + 'BusynessMonitor/getData',
                reader: {
                    type: 'json',
                    root: 'result'
                },
                timeout: 10000
            },
            fields: [{
                name: 'site',
                type: 'string'
            }, {
                name: 'max',
                type: 'int'
            }, {
                name: 'current',
                type: 'int'
            }, {
                name: 'week_done',
                type: 'int'
            }, {
                name: 'week_failed',
                type: 'int'
            }],
            autoLoad: true,
            pageSize: 20,

        });
        me.grid = Ext.create('Ext.grid.Panel', {
            region: 'center',
            store: me.dataStore,
            features: [{
                ftype: 'summary'
            }],
            header: false,
            columns: [{
                header: 'Site',
                sortable: true,
                dataIndex: 'site',
                align: 'left',
            }, {
                header: 'MaxJobs',
                sortable: true,
                dataIndex: 'max',
                align: 'left',
            }, {
                header: 'CurrentJobs',
                sortable: true,
                dataIndex: 'current',
                align: 'left',
            }, {
                header: 'WeekDoneJobs',
                sortable: true,
                dataIndex: 'week_done',
                align: 'left',
            }, {
                header: 'WeekFailedJobs',
                sortable: true,
                dataIndex: 'week_failed',
                align: 'left',
            }]
        });

        me.add([me.grid]);

    }
});
