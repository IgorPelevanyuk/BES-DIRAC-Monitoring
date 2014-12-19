Ext.define('DIRAC.Test.classes.Test', {
    extend : 'Ext.dirac.core.Module',
    requires :['Ext.panel.Panel', 'Ext.form.field.TextArea', 'Ext.Button', 'Ext.toolbar.Toolbar'],
    initComponent:function(){
      var me = this;

      me.launcher.title = "My First Application";
      me.launcher.maximized = false;
    
      me.launcher.width = 500;
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
      var me = this;

      me.leftPanel = new Ext.create('Ext.panel.Panel', {
        title : 'Text area',
        region : 'west',
        width : 250,
        minWidth : 230,
        maxWidth : 350,
        bodyPadding : 5,
        autoScroll : true,
        layout : {
            type : 'vbox',
            align : 'stretch',
            pack : 'start'
        }
      });

      me.textArea = new Ext.create('Ext.form.field.TextArea', {
        fieldLabel : "Value",
        labelAlign : "top",
        flex : 1
      });
      
      me.leftPanel.add(me.textArea);

      me.btnGetData = new Ext.Button({
        text : 'getData',
        margin : 1,
        handler : function() {
            Ext.Ajax.request({
                    url : GLOBAL.BASE_URL + 'Test/getData',
                    scope : me,
                    success : function(response) {
                            var me = this;
                            var response = Ext.JSON.decode(response.responseText);
                            alert("THE VALUE: "+response.result);
                    }
            });
        },
        scope : me
      });
      
      me.btnCreateDB = new Ext.Button({

        text : 'CreateInstance',
        margin : 1,
        handler : function() {
            Ext.Ajax.request({
                    url : GLOBAL.BASE_URL + 'Test/createDBinstance',
                    params : { },
                    scope : me,
                    success : function(response) {
                      alert("Instance created");
                    }
            });
        },
        scope : me
      });
      
      me.btnSetData = new Ext.Button({
        text : 'SetData',
        margin : 1,
        handler : function() {
            Ext.Ajax.request({
                    url : GLOBAL.BASE_URL + 'Test/setData',
                    params : {
                            value: me.textArea.getValue()
                    },
                    scope : me,
                    success : function(response) {
                            alert("Instance added");
                    }
            });
        },
        scope : me
      });
      
      var oPanelToolbar = new Ext.toolbar.Toolbar({
        dock : 'bottom',
        layout : {
            pack : 'center'
        },
        items : [me.btnCreateDB, me.btnGetData, me.btnSetData]
      });

      me.leftPanel.addDocked([oPanelToolbar]);
      
       me.dataStore = new Ext.data.JsonStore({

        proxy : {
            type : 'ajax',
            url : GLOBAL.BASE_URL + 'MyApp/getData',
            reader : {
                type : 'json',
                root : 'result'
            },
            timeout : 1800000
        },
        fields : [{
                    name : 'value',
                    type : 'int'
         }],
        autoLoad : true,
        pageSize : 50,

    });

      me.grid = Ext.create('Ext.grid.Panel', {
        region : 'center',
        store : me.dataStore,
        header : false,
        columns : [{
            header : 'Value',
            sortable : true,
            dataIndex : 'value',
            align : 'left'
        }]
    });

     me.add([me.leftPanel,me.grid]);
    
    }
});
