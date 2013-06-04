var ShowTimeSelectWin = function(searchFieldId) {
    var searchFormId = Ext.id();
    var searchStartDateFieldId = Ext.id();
    var searchEndDateFieldId = Ext.id();
    var timeSelectWin = new XG.Form.SimpelPoupWin({
        width: 260,
        autoHeight: true,
        layout: 'fit',
        title: '选择时间',
        resizable: false,
        items: [{
            xtype: 'form',
            labelAlign: 'right',
            labelWidth: 60,
            border: true,
            width: 250,
            padding: 15,
            autoHeight: true,
            buttonAlign: 'center',
            id: searchFormId,
            defaults: {
                width: 140
            },
            items: [
            DefaultDateFeild({
                id: searchStartDateFieldId,
                format: 'Y-m-d',
                fieldLabel: '起始时间'
            }),
            DefaultDateFeild({
                id: searchEndDateFieldId,
                format: 'Y-m-d',
                fieldLabel: '结束时间'
            })],
            buttons: [{
                text: '确 定',
                handler: function() {
                    var form = Ext.getCmp(searchFormId).getForm();
                    if (form.isValid()) {
                        var startDate = Ext.getCmp(searchStartDateFieldId).value;
                        var endDate = Ext.getCmp(searchEndDateFieldId).value;
                        Ext.getCmp(searchFieldId).setValue(String.format('{0}至{1}', startDate, endDate));
                        Ext.getCmp(searchFieldId).searchType = 'time';
                        timeSelectWin.close();
                    }
                }
            }, {
                text: '取 消',
                handler: function() {
                    timeSelectWin.close();
                }
            }]
        }]
    });
    timeSelectWin.on('show', function() {
        Ext.getCmp(searchFieldId).setValue('');
        Ext.getCmp(searchFieldId).getEl().dom.setAttribute('readOnly', true);
    });
    timeSelectWin.show();
};


var ShowUnitSelectWin = function(searchFieldId) {
    var searchFormId = Ext.id();
    var xcomboboxtreeId = Ext.id();
    var unitSelectWin = new XG.Form.SimpelPoupWin({
        width: 270,
        autoHeight: true,
        layout: 'fit',
        title: '选择部门',
        resizable: false,
        items: [{
            xtype: 'form',
            labelAlign: 'right',
            labelWidth: 60,
            border: true,
            width: 250,
            padding: 15,
            autoHeight: true,
            buttonAlign: 'center',
            id: searchFormId,
            defaults: {
                width: 140
            },
            items: [{
                xtype: 'xcomboboxtree',
                fieldLabel: '部门',
                allowBlank: false,
                id: xcomboboxtreeId,
                tree: {
                    height: 200,
                    autoScroll: true,
                    xtype: 'unittree',
                    url: '/logic/UnitHandler.ashx?f=ExpanUnitTree',
                    border: true,
                    rootVisible: false,
                    roottext: '选择部门',
                    listeners: {
                        click: function(f, v) {
                            Ext.getCmp(xcomboboxtreeId).hiddenValue = f.attributes.treeid;
                            if(f.attributes.level==3)
                            {
                                var parent = f.parentNode;
                                Ext.getCmp(xcomboboxtreeId).data = String.format('{0} > {1}',
                                    parent.attributes.text,
                                    f.attributes.text);
                            }else{
                                Ext.getCmp(xcomboboxtreeId).data = f.attributes.text;
                            }
                            
                        }
                    }
                }
            }],
            buttons: [{
                text: '确 定',
                handler: function() {
                    var form = Ext.getCmp(searchFormId).getForm();
                    if (form.isValid()) {
                        var unitId = Ext.getCmp(xcomboboxtreeId).hiddenValue;
                        var unitName = Ext.getCmp(xcomboboxtreeId).data;
                        var searField = Ext.getCmp(searchFieldId);
                        searField.setValue(unitName);
                        searField.searchType = 'unit';
                        searField.data = unitId;
                        unitSelectWin.close();
                    }
                }
            }, {
                text: '取 消',
                handler: function() {
                    unitSelectWin.close();
                }
            }]
        }]
    });
    unitSelectWin.on('show', function() {
        Ext.getCmp(searchFieldId).setValue('');
        Ext.getCmp(searchFieldId).getEl().dom.setAttribute('readOnly', true);
    });
    unitSelectWin.show();
};

var getLiveSearchItems = function(grid, searchType_storeData) {
    var searchFieldId = Ext.id();
    var searchTypeComboId = Ext.id();
    return [
        '关键字：', {
        xtype: 'textfield',
        name: searchFieldId,
        id: searchFieldId,
        hideLabel: true,
        width: 160
    }, {
        xtype: 'combo',
        id: searchTypeComboId,
        width: 130,
        editable: false,
        hideLabel: true,
        displayField: "text",
        valueField: "value",
        mode: "local",
        triggerAction: "all",
        emptyText: '请选择搜索项',
        store: new Ext.data.SimpleStore({
            fields: ['text', 'value', 'isDate', 'isUnit'],
            data: searchType_storeData
        }),
        listeners: {
            beforeselect: function(combo, record, index) {
                var lastSelectRecord = combo.findRecord(combo.valueField || combo.displayField, combo.getValue());
                if (record.data.isDate) {
                    ShowTimeSelectWin(searchFieldId);
                    return;
                } else if (record.data.isUnit) {
                    ShowUnitSelectWin(searchFieldId);
                    return;
                }

                if (lastSelectRecord && (lastSelectRecord.data.isDate || lastSelectRecord.data.isUnit)) {
                    Ext.getCmp(searchFieldId).setValue('');
                    Ext.getCmp(searchFieldId).getEl().dom.removeAttribute('readOnly');
                    return;
                }
            }
        }
    }, {
        xtype: 'button',
        text: '搜索',
        width: 50,
        iconCls: 'Magnifier',
        tooltip: '搜索',
        handler: function() {
            var keywords = Ext.getCmp(searchFieldId).getValue();
            if (!keywords) {
                alert('请输入查询关键字');
                return;
            }
            var comboVal = Ext.getCmp(searchTypeComboId).getValue();
            if (!comboVal) {
                alert('请选择搜索项');
                return;
            }
            var searchType = Ext.getCmp(searchFieldId).searchType;
            var searchCondition;
            if (!searchType) {
                searchCondition = String.format("{0} LIKE '{1}%'",
                Ext.getCmp(searchTypeComboId).value,
                keywords);
            } else if (searchType == 'time') {
                var dateArray = keywords.split('至');
                if (dateArray.length != 2) return;
                searchCondition = String.format("{0} BETWEEN '{1}' AND '{2}'",
                Ext.getCmp(searchTypeComboId).value,
                dateArray[0],
                dateArray[1]);
            } else if (searchType == 'unit') {
                var unitId = Ext.getCmp(searchFieldId).data
                if (!unitId) return;
                searchCondition = String.format("{0} = {1} ",
                Ext.getCmp(searchTypeComboId).value, unitId);
            }

            grid.getStore().load({
                params: {
                    start: 0,
                    limit: grid.getStore().pageSize,
                    searchCondition: searchCondition
                }
            });
        }
    },
        '-', {
        xtype: 'button',
        text: '显示全部',
        width: 60,
        handler: function() {
            grid.getStore().load({
                params: {
                    start: 0,
                    limit: 20
                }
            });
        }
    }];
};

Ext.ns("XG.Control.AbstractGrid");
XG.Control.AbstractGrid = Ext.extend(Ext.grid.GridPanel, {
    constructor: function(config) {
        var itemsPerPage = 20;
        var stroe_fields = ['ID'];
        var url = config.url;
        var columes = config.columes;
        var tbar = config.tbar;
        var baseParams = config.baseParams;
        var data_columes = [];
        var search_storeData = [];
        var grid = this;
        //no check
        if (!config.nocheck) {
            var sm_cfg = {
                singleSelect: false,
                sortable: false
            };
            if (config.refresh_tar) {
                sm_cfg.listeners = {
                    rowselect: config.refresh_tar,
                    rowdeselect: config.refresh_tar
                };
                this.refresh_tar = config.refresh_tar;
            }
            if (config.singleSelect) sm_cfg.singleSelect = true;
            var sm = new Ext.grid.CheckboxSelectionModel(sm_cfg);
            this.selModel = sm;
            data_columes.push(sm);
        }
        for (var i in columes) {
            var column = columes[i]
            stroe_fields.push(column.dataIndex);
            if (column.hasOwnProperty('header')) {
                data_columes.push(column);
            }
            if (column.expand) {
                config.autoExpandColumn = column.id = Ext.id();
            }
            if (column.hasOwnProperty('search')) {
                if (column.search) {
                    var isDate = column.hasOwnProperty('isDate') ? true : false;
                    var isUnit = column.hasOwnProperty('isUnit') ? true : false;
                    var text = column.hasOwnProperty('text') ? column.text : column.header;
                    var value = column.hasOwnProperty('value') ? column.value : column.dataIndex;
                    search_storeData.push([text, value, isDate, isUnit]);
                }
            }
        }

        var toolbar = [];
        if (search_storeData.length > 0) {
            toolbar = getLiveSearchItems(grid, search_storeData);
            if (tbar) toolbar.push('-');
        }


        if (isArrary(tbar)) {
            toolbar = toolbar.concat(tbar);
        } else {
            var control;
            for (var method in tbar) {
                if (!(method in this)) continue;
                if (isArrary(tbar[method])) {
                    for (var i in tbar[method]) {
                        control = this[method](tbar[method][i]);
                        toolbar.push(control);
                    }
                } else {
                    control = this[method](tbar[method]);
                    toolbar.push(control);
                }
            }
        }

        var store = {
            totalProperty: 'total',
            idProperty: 'pk',
            fields: stroe_fields,
            root: 'items',
            pageSize: itemsPerPage,
            proxy: new Ext.data.HttpProxy({
                type: 'ajax',
                url: config.url
            })
        };
        if (config.store_listeners) store.listeners = config.store_listeners;
        var store = new Ext.data.JsonStore(store);
        if (baseParams) {
            store.baseParams = baseParams;
        }
        var init_config = {
            stateful: true,
            multiSelect: true,
            store: store,
            border: false,
            cm: new Ext.grid.ColumnModel(data_columes),
            region: 'center',
            viewConfig: {
                //forceFit:true,
                stripeRows: true,
                enableTextSelection: true
            }
        };
        if (config.width) init_config.width = config.width;
        if (config.height) init_config.height = config.height;
        if (config.border) init_config.border = true;
        if (config.id) init_config.id = config.id;
        if (toolbar.length > 0) init_config.tbar = toolbar;
        if (config.hasOwnProperty('autoExpandColumn')) {
            init_config.autoExpandColumn = config.autoExpandColumn;
        }
        if (!config.nopage) {
            init_config.bbar = new Ext.PagingToolbar({
                pageSize: itemsPerPage,
                store: store,
                displayInfo: true
            });
        }
        XG.Control.AbstractGrid.superclass.constructor.call(this, init_config);
        if (config.listeners) {
            for (var i in config.listeners)
            this.addListener(i, config.listeners[i]);
        }
    },
    getIdArray: function() {
        var record = this.getSelectionModel().getSelections();
        if (!record || 0 == record.length) {
            alert('没有选中任数据!');
            return null;
        }
        var ids = [];
        Ext.each(record, function(item) {
            ids.push(item.json.pk);
        });
        return ids;
    },
    getFirstId: function() {
        var ids = this.getIdArray();
        if (ids != null) {
            return ids[0];
        }
        return null;
    },
    getSelect: function() {
        var record = this.getSelectionModel().getSelections();
        var sel_records = [];
        if (record && record.length > 0) {
            Ext.each(record, function(item) {
                sel_records.push(item);
            });
        }
        return sel_records;
    },
    del_row: function(config) {
        var iconCls = config.hasOwnProperty('iconCls') ? config.iconCls : 'Databasedelete';
        var grid = this;
        return {
            text: config.text,
            iconCls: iconCls,
            handler: function() {
                var ids = grid.getIdArray();
                if (ids == null) return;
                confirm(config.alert, function(e) {
                    Ext.Ajax.request({
                        url: config.url,
                        method: "post",
                        params: {
                            ids: ids.join()
                        },
                        success: function() {
                            grid.getStore().reload();
                            if (config.success) alert(config.success);
                            else alert('删除成功!');
                        },
                        failure: function(form, action) {
                            if ('result' in action) {
                                if ('msg' in action.result) {
                                    error(action.result.msg);
                                }
                            } else {
                                error('发生异常!');
                            }
                        }
                    });
                });
            }
        }
    }
});
Ext.reg('basegrid', XG.Control.AbstractGrid);



Ext.ns("LD.Control.AbstractEditorGrid");
LD.Control.BaseEditorGrid = Ext.extend(Ext.grid.EditorGridPanel, {
    constructor: function(config) {
        var itemsPerPage = 20;
        var stroe_fields = ['ID'];
        var url = config.url;
        var columns = config.columns;
        var tbar = config.tbar;
        var baseParams = config.baseParams;
        var data_columns = [];
        //no check
        if (!config.nocheck) {
            var sm_cfg = {
                singleSelect: false,
                sortable: false
            };
            if (config.refresh_tar) sm_cfg.listeners = {
                rowselect: config.refresh_tar,
                rowdeselect: config.refresh_tar
            };
            if (config.singleSelect) sm_cfg.singleSelect = true;
            var sm = new Ext.grid.CheckboxSelectionModel(sm_cfg);
            this.selModel = sm;
            data_columns.push(sm);
        }
        for (var i in columns) {
            stroe_fields.push(columns[i].dataIndex);
            if (columns[i].hasOwnProperty('header')) {
                data_columns.push(columns[i]);
            }
            if (columns[i].expand) {
                config.autoExpandColumn = columns[i].id = Ext.id();
            }

            if (columns[i].hasOwnProperty('editorConfig')) {
                var editorConfig = columns[i].editorConfig;
                if (editorConfig.xtype == 'combo') {
                    columns[i].editor = new Ext.form.ComboBox(editorConfig);
                } else {
                    columns[i].editor = new Ext.form.TextField(editorConfig);
                }

            }
        }

        var toolbar;
        if (isArrary(tbar)) {
            toolbar = tbar;
        } else {
            toolbar = []
            var control;
            for (var method in tbar) {
                if (!(method in this)) continue;
                if (isArrary(tbar[method])) {
                    for (var i in tbar[method]) {
                        control = this[method](tbar[method][i]);
                        toolbar.push(control);
                    }
                } else {
                    control = this[method](tbar[method]);
                    toolbar.push(control);
                }
            }
        }
        var store = {
            totalProperty: 'total',
            idProperty: 'pk',
            fields: stroe_fields,
            root: 'items',
            pageSize: itemsPerPage,
            proxy: new Ext.data.HttpProxy({
                type: 'ajax',
                url: config.url
            }),
            autoLoad: true
        };
        if (config.store_listeners) store.listeners = config.store_listeners;
        var store = new Ext.data.JsonStore(store);

        if (baseParams) {
            store.baseParams = baseParams;
        }
        var init_config = {
            stateful: true,
            multiSelect: true,
            store: store,
            border: false,
            cm: new Ext.grid.ColumnModel(data_columns),
            region: 'center',
            viewConfig: {
                stripeRows: true,
                enableTextSelection: true
            }
        };
        if (config.width) init_config.width = config.width;
        if (config.height) init_config.height = config.height;
        if (config.border) init_config.border = true;
        if (config.id) init_config.id = config.id;
        if (config.autoHeight) init_config.autoHeight = config.autoHeight;
        if (config.style) init_config.style = config.style;
        if (config.hideHeaders) init_config.hideHeaders = config.hideHeaders;
        if (config.buttons) init_config.buttons = config.buttons;
        if (config.buttonAlign) init_config.buttonAlign = config.buttonAlign;
        if (toolbar.length > 0) init_config.tbar = toolbar;
        if (config.hasOwnProperty('autoExpandColumn')) {
            init_config.autoExpandColumn = config.autoExpandColumn;
        }
        if (!config.nopage) {
            init_config.bbar = new Ext.PagingToolbar({
                pageSize: itemsPerPage,
                store: store,
                displayInfo: true
            });
        }
        XG.Control.AbstractGrid.superclass.constructor.call(this, init_config);
        if (config.listeners) {
            for (var i in config.listeners)
            this.addListener(i, config.listeners[i]);
        }
    },
    listeners: {
        validateedit: function(e) {
            var grid = e.grid;
            // alert('ok');
        }
    },
    getIdArray: function() {
        var record = this.getSelectionModel().getSelections();
        if (!record || 0 == record.length) {
            alert('没有选中任数据!');
            return null;
        }
        var ids = [];
        Ext.each(record, function(item) {
            ids.push(item.json.pk);
        });
        return ids;
    },
    getFirstId: function() {
        var ids = this.getIdArray();
        if (ids != null) {
            return ids[0];
        }
        return null;
    },
    getSelect: function() {
        var record = this.getSelectionModel().getSelections();
        var sel_records = [];
        if (record && record.length > 0) {
            Ext.each(record, function(item) {
                sel_records.push(item);
            });
        }
        return sel_records;
    }
});
Ext.reg('baseeditorgrid', LD.Control.BaseEditorGrid);


Ext.namespace("XG.Renders");
XG.Renders.ShowFolder = function(value) {
    var tree = Main.CurrentTree();
    var node = tree.currentnode;
    var cur_node = node.findChild('text', value);
    cur_node.fireEvent('click', cur_node);
}
XG.Renders.FileNameRender = function(value, cellmeta, record, rowIndex, columnIndex, store) {
    if (record.data.IsDir == "1") {
        var str = '<img   src="';
        str += '/ext/resources/images/default/tree/folder.gif';
        str += '"  onerror="this.src=\'/images/fext/unknown_16.gif\'"> ';
        str += '<a href="javascript:XG.Renders.ShowFolder(\'' + value + '\')">' + value + '</a>';
        str += '</img>';
        return str;
    } else {
        var ext = fileExt(value);
        ext = '/images/fext/' + ext + '_16.gif';
        var str = '<img src="';
        str += ext;
        str += '"  onerror="this.src=\'/images/fext/unknown_16.gif\'"> ';
        str += value;
        str += '</img>';
        return str;
    }
}.createDelegate(this);

XG.Renders.FileSizeRender = function(value) {
    if (value == "") return "";
    return accounting.formatNumber(value) + '字节'
}.createDelegate(this);

XG.Renders.FileAuthRender = function(value) {
    if (value == 0) return "";
    var str = [];
    if ((8 & value) == 8) str.push("预览");
    if ((4 & value) == 4) str.push("编辑");
    if ((1 & value) == 1) str.push("截屏");
    if ((2 & value) == 2) str.push("下载");
    if ((16 & value) == 16) str.push("打印");
    return str.join();
};

function RawAuthCodeJson(value) {
    return {
        look: (8 & value) == 8,
        edit: (4 & value) == 4,
        cutscreen: (1 & value) == 1,
        download: (2 & value) == 2,
        print: (16 & value) == 16
    };
}

function RawAuthCode(auth) {
    var code = 0;
    code = auth.look ? code | 8 : code & ~8;
    code = auth.edit ? code | 4 : code & ~4;
    code = auth.cutscreen ? code | 1 : code & ~1;
    code = auth.download ? code | 2 : code & ~2;
    code = auth.print ? code | 16 : code & ~16;
    return code;
}

XG.Renders.UserRender = function(value) {
    if (value == "") return "";
    value = Ext.util.Format.htmlEncode(value);
    return '<img src="/ext/icons/user.gif"> ' + value + '</img>';
}.createDelegate(this);


XG.Renders.ToUserRender = function(value) {
    if (value == "") return "";
    value = Ext.util.Format.htmlEncode(value);
    return '<img src="/ext/icons/user_tick.gif"> ' + value + '</img>';
}.createDelegate(this);

XG.Renders.FileLockerRender = function(value) {
    if (value == "") return "";
    value = Ext.util.Format.htmlEncode(value);
    return '<img src="/ext/icons/user_go.gif"> ' + value + '</img>';
}.createDelegate(this);

XG.Renders.CreaterRender = function(value) {
    if (value == "") return "";
    value = Ext.util.Format.htmlEncode(value);
    return '<img src="/ext/icons/user.gif"> ' + value + '</img>';
}.createDelegate(this);

XG.Renders.UploaderRender = function(value) {
    if (value == "") return "";
    value = Ext.util.Format.htmlEncode(value);
    return '<img src="/ext/icons/user.gif"> ' + value + '</img>';
}.createDelegate(this);

Ext.ns("XG.Control.RemoteCombo");
XG.Control.RemoteCombo = Ext.extend(Ext.form.ComboBox, {
    constructor: function(config) {
        this.name = config.name;
        this.url = config.url;
        this.baseParams = config.baseParams;
        this.loadCallback = this.loadCallback;
        XG.Control.RemoteCombo.superclass.constructor.call(this, config);
    },
    initComponent: function() {
        var fileds = [{
            name: 'pk',
            mapping: 'pk',
            type: 'int'
        }, {
            name: 'name',
            mapping: 'name',
            type: 'string'
        }];
        if (this.baseFields) {
            for (var i = 0; i < this.baseFields.length; i++) {
                fileds.push(this.baseFields[i]);
            }
        }
        var reader = new Ext.data.JsonReader({
            root: "items",
            fields: fileds
        });
        var name = this.name,
            url = this.url;
        var proxy = new Ext.data.HttpProxy({
            type: 'ajax',
            url: url
        });
        var store = new Ext.data.Store({
            baseParams: this.baseParams,
            proxy: proxy,
            reader: reader
        });
        Ext.apply(this, {
            hiddenName: name,
            store: store,
            valueField: 'pk',
            triggerAction: 'all',
            displayField: 'name',
            mode: 'local',
            editable: false
        });
        var combo = this;
        store.load({
            callback: function(r, option, success) {
                if (success && r.length > 0) {
                    combo.setValue(store.getAt(0).data.pk);
                }
                if (combo.loadCallback) combo.loadCallback();

            }
        });
    },
    setValue: function(v) {
        var text = v;
        if (this.valueField) {
            var r = this.findRecord(this.valueField, v);
            if (r) {
                text = r.data[this.displayField];
            } else if (this.valueNotFoundText !== undefined) {
                text = this.valueNotFoundText;
            }
        }
        this.lastSelectionText = text;
        if (this.hiddenField) {
            this.hiddenField.value = v;
        }
        // new code here
        if (this.unEscapeValue) {
            text = text.unescapeHTML();
        }
        Ext.form.ComboBox.superclass.setValue.call(this, text);
        this.value = v;
    }
});
Ext.reg('remotecombo', XG.Control.RemoteCombo);

Ext.ns("XG.Control.LocalCombo");
XG.Control.LocalCombo = Ext.extend(Ext.form.ComboBox, {
    constructor: function(config) {
        this.data = config.data;
        this.name = config.name;
        XG.Control.LocalCombo.superclass.constructor.call(this, config);
    },
    initComponent: function() {
        var store = new Ext.data.SimpleStore({
            fields: ['value', 'text'],
            data: this.data
        });
        Ext.apply(this, {
            hiddenName: this.name,
            name: this.name + '_s',
            store: store,
            valueField: 'value',
            triggerAction: 'all',
            displayField: 'text',
            mode: 'local',
            editable: false,
            value: this.data[0][0]
        });
    }
});
Ext.reg('localcombo', XG.Control.LocalCombo);

function DefaultDateFeild(config) {
    if (!config) config = {};
    config.xtype = 'datefield';
    config.editable = false;
    config.altFormats = 'Y年m月d日';
    config.format = config.format ? config.format : 'Y年m月d日';
    config.allowBlank = config.allowBlank ? true : false;
    return config;
}


Ext.ns("XG.Control.BaseLeftTree");
XG.Control.BaseLeftTree = Ext.extend(Ext.tree.TreePanel, {
    constructor: function(config) {
        this.fields = ['list', 'text', 'view'];
        this.currentid = null;
        this.useArrows = true;
        this.autoScroll = true;
        this.animate = true;

        this.containerScroll = true;
        this.border = false;
        this.view = config.view;
        this.rootVisible = config.rootVisible;
        this.loader = new Ext.tree.TreeLoader();

        this.root = {
            nodeType: 'async',
            text: config.roottext,
            treeid: '0',
            children: config.children
        };
        XG.Control.BaseLeftTree.superclass.constructor.call(this, config);
    },
    listeners: {
        click: function(node, e) {
            if (node.attributes.list || node.attributes.view) {
                var exisTab = Main.Center.findById(node.attributes.text);
                if (!exisTab) {
                    if (node.attributes.list) {
                        var grid = new XG.Control.AbstractGrid(node.attributes.list);
                        grid.getStore().load({
                            params: {
                                start: 0,
                                limit: 20
                            }
                        });
                    } else if (node.attributes.view) {
                        grid = node.attributes.view;
                    }
                    exisTab = Main.Center.add({
                        closable: true,
                        id: node.attributes.text,
                        title: node.attributes.text,
                        layout: {
                            type: 'fit'
                        },
                        items: [grid]
                    });
                    exisTab.show();
                }
                Main.Center.setActiveTab(exisTab);
            }
        }
    }
});
Ext.reg('baselefttree', XG.Control.BaseLeftTree);


Ext.ns("XG.Control.FolderTreeLoader");
XG.Control.FolderTreeLoader = Ext.extend(Ext.tree.TreeLoader, {
    constructor: function(config) {
        XG.Control.FolderTreeLoader.superclass.constructor.call(this, config);
    },
    getParams: function(node) {
        var buf = [],
            bp = this.baseParams;
        if (this.directFn) {
            buf.push(node.attributes.treeid);
            if (bp) {
                if (this.paramOrder) {
                    for (var i = 0, len = this.paramOrder.length; i < len; i++) {
                        buf.push(bp[this.paramOrder[i]]);
                    }
                } else if (this.paramsAsHash) {
                    buf.push(bp);
                }
            }
            return buf;
        } else {
            for (var key in bp) {
                if (!Ext.isFunction(bp[key])) {
                    buf.push(encodeURIComponent(key), "=", encodeURIComponent(bp[key]), "&");
                }
            }
            buf.push("node=", encodeURIComponent(node.attributes.treeid));
            return buf.join("");
        }
    },
    processResponse: function(response, node, callback, scope) {
        var json = response.responseText;
        try {
            var o = response.responseData || Ext.decode(json);
            node.beginUpdate();
            for (var i = 0, len = o.length; i < len; i++) {
                o[i].iconCls = 'Folderpage';
                var n = this.createNode(o[i]);
                if (n) {
                    node.appendChild(n);
                }
            }
            node.endUpdate();

            this.runCallback(callback, scope || node, [node]);
        } catch (e) {
            this.handleFailure(response);
        }
    }
});

Ext.ns("XG.Control.FolderTree");
XG.Control.FolderTree = Ext.extend(Ext.tree.TreePanel, {
    constructor: function(config) {
        this.fields = ['text', 'treeid'];
        this.currentid = null;
        this.currentnode = null;
        this.useArrows = true;
        this.autoScroll = true;
        this.animate = true;
        this.containerScroll = true;
        this.border = false;
        this.view = config.view;
        this.loader = new XG.Control.FolderTreeLoader({
            url: config.url
        });
        this.root = {
            nodeType: 'async',
            text: config.roottext,
            treeid: '0'
        };
        XG.Control.FolderTree.superclass.constructor.call(this, config);
    },
    listeners: {
        click: function(node, e) {
            var exisTab = Main.Center.findById(this.tab_id);
            var refresh_tar = this.view.refresh_tar;

            function loadNode(grid_id) {
                exisTab.setTitle('正在加载...');
                var grid = Ext.getCmp(grid_id);

                grid.getStore().load({
                    params: {

                        start: 0,
                        limit: 20
                    },
                    callback: function(o, response, success) {
                        exisTab.setTitle(node.attributes.text);
                    }
                });
            }
            if (!exisTab) {
                this.tab_id = Ext.id();
                this.grid_id = this.view.id = Ext.id();

                exisTab = Main.Center.add({
                    closable: true,
                    id: this.tab_id,
                    title: node.attributes.text,
                    layout: {
                        type: 'fit'
                    },
                    items: [this.view]
                });
                exisTab.treeid = this.id;
                exisTab.show();
                this.currentid = node.attributes.treeid;
                this.currentnode = node;
                loadNode(this.grid_id);
            } else if (this.currentid != node.attributes.treeid) {
                this.currentid = node.attributes.treeid;
                this.currentnode = node;
                loadNode(this.grid_id);
            }

            Main.Center.setActiveTab(exisTab);
        }
    }
});
Ext.reg('foldertree', XG.Control.FolderTree);


Ext.ns("XG.Control.UnitTreeLoader");
XG.Control.UnitTreeLoader = Ext.extend(Ext.tree.TreeLoader, {
    constructor: function(config) {
        this.checked_user = config.checked_user;
        this.checked_unit = config.checked_unit;
        this.checked_unit_folder = config.checked_unit_folder;
        XG.Control.UnitTreeLoader.superclass.constructor.call(this, config);
    },
    createNode: function(attr) {
        if (attr.type == 'unit') attr.iconCls = 'Userhome';
        else if (attr.type == 'unitfolder') attr.iconCls = 'Folderhome';
        else if (attr.type == 'unituser') attr.iconCls = 'User';
        return XG.Control.UnitTreeLoader.superclass.createNode.call(this, attr);
    },
    processResponse: function(response, node, callback) {
        node.beginUpdate();
        try {
            var jsonObj = Ext.util.JSON.decode(response.responseText);
            var o = jsonObj.units;
            if (o) {
                for (var i = 0; i < o.length; i++) {
                    o[i].type = 'unit';
                    if (this.checked_unit) o[i].checked = false;
                    node.appendChild(o[i]);
                }
            }
            o = jsonObj.folders;
            if (o) {
                for (var i = 0; i < o.length; i++) {
                    o[i].type = 'unitfolder';
                    o[i].leaf = true;
                    if (this.checked_unit_folder) o[i].checked = false;
                    o[i].unit_node = node;
                    node.appendChild(o[i]);
                }
            }
            o = jsonObj.users;
            if (o) {
                for (var i = 0; i < o.length; i++) {
                    o[i].type = 'unituser';
                    o[i].leaf = true;
                    if (this.checked_user) o[i].checked = false;
                    o[i].unit_node = node;
                    o[i].fullname = encodehtml(o[i].text);
                    o[i].text = o[i].text.substring(0, o[i].text.indexOf('<'));
                    node.appendChild(o[i]);
                }
            }
            if (typeof(callback) == "function") {
                callback(this, node);
            }
        } catch (e) {
            this.handleFailure(response);
        } finally {
            node.endUpdate();
        }
    },
    getParams: function(node) {
        var buf = [],
            bp = this.baseParams;
        if (this.directFn) {
            buf.push(node.attributes.treeid);
            buf.push(node.attributes.type);
            if (bp) {
                if (this.paramOrder) {
                    for (var i = 0, len = this.paramOrder.length; i < len; i++) {
                        buf.push(bp[this.paramOrder[i]]);
                    }
                } else if (this.paramsAsHash) {
                    buf.push(bp);
                }
            }
            return buf;
        } else {
            for (var key in bp) {
                if (!Ext.isFunction(bp[key])) {
                    buf.push(encodeURIComponent(key), "=", encodeURIComponent(bp[key]), "&");
                }
            }
            buf.push("type=", encodeURIComponent(node.attributes.type), "&");
            buf.push("node=", encodeURIComponent(node.attributes.treeid));
            return buf.join("");
        }
    }
});

Ext.ns("XG.Control.UnitTree");
XG.Control.UnitTree = Ext.extend(Ext.tree.TreePanel, {
    constructor: function(config) {
        this.fields = ['text', 'treeid', 'type', 'unit_node', 'level', 'fullname'];
        this.currentid = null;
        this.useArrows = true;
        this.autoScroll = true;
        this.animate = true;
        this.containerScroll = true;
        this.border = false;
        this.view = config.view;
        this.checked = config.checked;
        if (config.singleChecked) {
            config.listeners = {
                checkchange: function(node, e) {
                    var checked = this.getChecked();
                    for (var i = 0; i < checked.length; i++) {
                        checked[i].getUI().checkbox.checked = false;
                    }
                    node.getUI().checkbox.checked = !node.getUI().checkbox.checked;
                }
            }
        }
        if (config.url) {
            this.loader = new XG.Control.UnitTreeLoader({
                url: config.url,
                checked_user: config.checked_user,
                checked_unit: config.checked_unit,
                checked_unit_folder: config.checked_unit_folder
            });
        }
        if (config.view) {
            this.view = config.view;
            config.listeners = {
                click: function(node, e) {

                    var exisTab = Main.Center.findById(this.tab_id);
                    var refresh_tar = this.view.refresh_tar;

                    function loadNode(grid_id) {
                        exisTab.setTitle('正在加载...');
                        var grid = Ext.getCmp(grid_id);
                        node.expand();

                        grid.getStore().load({
                            params: {
                                node: node.attributes.treeid,
                                start: 0,
                                limit: 20
                            },
                            callback: function(o, response, success) {
                                exisTab.setTitle(node.attributes.text);
                            }
                        });
                    }
                    if (!exisTab) {
                        this.tab_id = Ext.id();
                        this.grid_id = this.view.id = Ext.id();
                        exisTab = Main.Center.add({
                            closable: true,
                            id: this.tab_id,
                            title: node.attributes.text,
                            layout: {
                                type: 'fit'
                            },
                            items: [this.view]
                        });
                        exisTab.treeid = this.id;
                        exisTab.show();
                        loadNode(this.grid_id);
                    } else if (this.currentid != node.attributes.treeid) {
                        loadNode(this.grid_id);
                    }
                    this.currentid = node.attributes.treeid;
                    this.currentnode = node;
                    Main.Center.setActiveTab(exisTab);
                }
            };
        }
        this.root = {
            nodeType: 'async',
            text: config.roottext,
            treeid: '0'
        };
        XG.Control.UnitTree.superclass.constructor.call(this, config);
    }
});
Ext.reg('unittree', XG.Control.UnitTree);


Ext.ns("XG.Control.ComboBoxTree");
XG.Control.ComboBoxTree = Ext.extend(Ext.form.TwinTriggerField, {
    animate: {
        easing: 'easeIn',
        duration: 0.75
    },
    defaultAutoCreate: {
        tag: "input",
        type: "text",
        size: "24",
        autocomplete: "off"
    },
    editable: false,
    enableClearValue: false,
    hiddenValue: '',
    displayValue: '',
    listWidth: undefined,
    listHeight: undefined,
    maxListHeight: 225,
    minListWidth: 70,
    handleHeight: 8,
    listClass: '',
    selectedClass: 'x-combo-selected',
    shadow: 'sides',
    listAlign: 'tl-bl?',
    listEmptyText: '',
    resizable: false,
    trigger1Class: 'x-form-clear-trigger',
    hideTrigger1: true,
    trigger2Class: 'x-form-arrow-trigger',
    initComponent: function() {
        this.addEvents('expand', 'collapse', 'treenodeselect', 'beforecollapse', 'beforeexpand', 'clearvalue');
        XG.Control.ComboBoxTree.superclass.initComponent.call(this);
        this.tree = Ext.create(this.tree);
        this.tree.height = Ext.isDefined(this.tree.height) ? this.tree.height : this.listHeight;
        this.tree.autoHeight = false;
        this.tree.autoScroll = true;
        this.tree.containerScroll = true;
        this.tree.border = false;
        this.tree.root.expanded = !Ext.isDefined(this.tree.height) ? true : this.tree.root.expanded;
        this.tplId = Ext.id();
        this.tpl = '<div id="' + this.tplId + '"></div>';
        this.onTrigger2Click = this.onTriggerClick;
        this.onTrigger1Click = this.clearValue;
    },
    onRender: function(ct, position) {
        if (this.hiddenName && !Ext.isDefined(this.submitValue)) {
            this.submitValue = false;
        }
        XG.Control.ComboBoxTree.superclass.onRender.call(this, ct, position);
        if (this.hiddenName) {
            var formItem = this.el.findParent('.x-form-item', 4, true);
            if (formItem) {
                this.hiddenField = formItem.insertSibling({
                    tag: 'input',
                    type: 'hidden',
                    name: this.hiddenName,
                    id: (this.hiddenId || this.hiddenName)
                }, 'after', true);
                var hf = new Ext.form.Hidden({
                    applyTo: this.hiddenField
                });
                var basicForm = this.getOwnerForm(this);
                if (basicForm) {
                    basicForm.add(hf);
                }
            } else {
                this.hiddenField = this.el.insertSibling({
                    tag: 'input',
                    type: 'hidden',
                    name: this.hiddenName,
                    id: (this.hiddenId || this.hiddenName)
                }, 'before', true);
            }
        }
        if (Ext.isGecko) {
            this.el.dom.setAttribute('autocomplete', 'off');
        }
        this.initList();
    },
    initList: function() {
        if (!this.list) {
            var cls = 'x-combo-list',
                listParent = Ext.getDom(this.getListParent() || Ext.getBody()),
                zindex = parseInt(Ext.fly(listParent).getStyle('z-index'), 10);
            if (!zindex) {
                zindex = this.getParentZIndex();
            }
            this.list = new Ext.Layer({
                parentEl: listParent,
                shadow: this.shadow,
                cls: [cls, this.listClass].join(' '),
                constrain: false,
                zindex: (zindex || 12000) + 5
            });
            var lw = this.listWidth || Math.max(this.wrap.getWidth(), this.minListWidth);
            this.list.setSize(lw, 0);
            this.tree.width = lw - 1;
            this.list.swallowEvent('mousewheel');
            this.assetHeight = 0;
            if (this.syncFont !== false) {
                this.list.setStyle('font-size', this.el.getStyle('font-size'));
            }
            if (this.title) {
                this.header = this.list.createChild({
                    cls: cls + '-hd',
                    html: this.title
                });
                this.assetHeight += this.header.getHeight();
            }
            this.innerList = this.list.createChild({
                cls: cls + '-inner'
            });
            this.innerList.setWidth(lw - this.list.getFrameWidth('lr'));
            this.view = new Ext.DataView({
                applyTo: this.innerList,
                tpl: this.tpl,
                singleSelect: true,
                selectedClass: this.selectedClass,
                itemSelector: this.itemSelector || '.' + cls + '-item',
                emptyText: this.listEmptyText,
                deferEmptyText: false,
                listeners: {
                    'afterrender': function() {
                        this.tpl.overwrite(this.el, []);
                    }
                }
            });
            this.mon(this.view, {
                containerclick: this.onViewClick,
                click: this.onViewClick,
                scope: this
            });
            if (this.resizable) {
                this.resizer = new Ext.Resizable(this.list, {
                    pinned: true,
                    handles: 'se'
                });
                this.mon(this.resizer, 'resize', function(r, w, h) {
                    this.maxHeight = h - this.handleHeight - this.list.getFrameWidth('tb') - this.assetHeight;
                    this.listWidth = w;
                    this.innerList.setWidth(w - this.list.getFrameWidth('lr'));
                    this.restrictHeight();
                }, this);
            }
        }
    },
    initEvents: function() {
        XG.Control.ComboBoxTree.superclass.initEvents.call(this);
        this.tree.on({
            scope: this,
            'render': function() {
                this.tree.getTreeEl().on('click', function(e, t, o) {
                    if (e.getTarget('.x-tree-ec-icon', 1)) { //is click tree's collapse/expand trigger icon area?
                        this.isTreeNodeClicked = false;
                    } else {
                        this.isTreeNodeClicked = true;
                    }
                }, this);
            },
            'click': function(n, e) {
                if (this.enableClearValue) {
                    this.triggers[0].show();
                }
                this.setValue(n.text);
                if (this.hiddenField) {
                    this.setHiddenValue(Ext.value(n.id, ''));
                }
                this.fireEvent('treenodeselect', this, n, e);
            }
        });
        this.tree.root.on({
            scope: this,
            'expand': {
                fn: function() {
                    if (!Ext.isDefined(this.tree.height)) { //dropdown list auto height
                        this.restrictHeight();
                    }
                },
                single: true
            }
        });
        this.on({
            'beforecollapse': {
                fn: function() {
                    if (!this.isExpanded()) {
                        return;
                    }
                    return this.isTreeNodeClicked;
                }
            },
            'beforedestroy': {
                fn: function() {
                    this.purgeListeners();
                    this.tree.purgeListeners();
                }
            },
            'beforeexpand': {
                fn: function() {
                    if (this.tree.rendered && !this.tree.getRootNode().isExpanded()) {
                        this.tree.getRootNode().expand(false, true);
                    }
                },
                single: true
            },
            'focus': {
                fn: function() {
                    if (!this.tree.rendered && this.tplId) {
                        this.tree.render(this.tplId);
                    }
                },
                single: true
            }
        });
    },
    initValue: function() {
        XG.Control.ComboBoxTree.superclass.initValue.call(this);
        if (this.hiddenField) {
            this.setHiddenValue(Ext.value(Ext.isDefined(this.hiddenValue) ? this.hiddenValue : this.value, ''));
        }
    },
    getOwnerForm: function(c) {
        var formPanel = this.findDirectFormOwnerCt(c);
        if (formPanel && formPanel.getForm()) {
            return formPanel.getForm();
        } else {
            return null;
        }
    },
    findDirectFormOwnerCt: function(c) {
        if (c.ownerCt) {
            if (c.ownerCt.getXType() == 'form') {
                return c.ownerCt;
            } else {
                return this.findDirectFormOwnerCt(c.ownerCt);
            }
        } else {
            return null;
        }
    },
    getListParent: function() {
        return document.body;
    },
    getParentZIndex: function() {
        var zindex;
        if (this.ownerCt) {
            this.findParentBy(function(ct) {
                zindex = parseInt(ct.getPositionEl().getStyle('z-index'), 10);
                return !!zindex;
            });
        }
        return zindex;
    },
    restrictHeight: function() {
        this.innerList.dom.style.height = '';
        var inner = this.innerList.dom,
            pad = this.list.getFrameWidth('tb') + (this.resizable ? this.handleHeight : 0) + this.assetHeight,
            h = Math.max(inner.clientHeight, inner.offsetHeight, inner.scrollHeight),
            ha = this.getPosition()[1] - Ext.getBody().getScroll().top,
            hb = Ext.lib.Dom.getViewHeight() - ha - this.getSize().height,
            space = Math.max(ha, hb, this.minHeight || 0) - this.list.shadowOffset - pad;

        h = Math.min(h, space, this.maxListHeight);

        this.innerList.setHeight(h);
        this.list.beginUpdate();
        this.list.setHeight(h + pad);
        this.list.alignTo.apply(this.list, [this.el].concat(this.listAlign));
        this.list.endUpdate();
    },
    isExpanded: function() {
        return this.list && this.list.isVisible();
    },
    onViewClick: function(doFocus) {
        var index = this.view.getSelectedIndexes()[0];
        if (!index) {
            this.collapse();
        }
        if (doFocus == true) {
            this.el.focus();
        }
    },
    onDestroy: function() {
        Ext.destroy(
        this.resizer, this.view, this.list);
        Ext.destroyMembers(this, 'hiddenField');
        XG.Control.ComboBoxTree.superclass.onDestroy.call(this);
    },
    setValue: function(val) {
        val = Ext.value(val, '');
        if (val != '') {
            if (this.enableClearValue) {
                this.triggers[0].show();
            }
        } else {
            if (this.enableClearValue) {
                this.triggers[0].hide();
            }
        }
        XG.Control.ComboBoxTree.superclass.setValue.call(this, val);
    },
    setHiddenValue: function(val) {
        val = Ext.value(val, '');
        if (val != '') {
            if (this.enableClearValue) {
                this.triggers[0].show();
            }
        } else {
            if (this.enableClearValue) {
                this.triggers[0].hide();
            }
        }
        if (this.hiddenField) {
            this.hiddenField.value = val;
            this.value = val;
        }
        return this;
    },
    reset: function() {
        XG.Control.ComboBoxTree.superclass.reset.call(this);
        if (this.hiddenField) {
            this.setHiddenValue('');
        }
    },
    clearValue: function() {
        if (this.enableClearValue) {
            var v = this.value;
            if (this.hiddenField) {
                v = this.hiddenField.value;
                this.hiddenField.value = '';
            }
            this.setValue('');
            this.validate();
            this.fireEvent('clearvalue', this, v);
        }
    },
    getTree: function() {
        return this.tree;
    },
    getValue: function() {
        if (this.hiddenField) {
            return Ext.isDefined(this.value) ? this.value : '';
        } else {
            return Ext.form.ComboBox.superclass.getValue.call(this);
        }
    },
    collapse: function() {
        if (!this.isExpanded()) {
            return;
        }

        if (this.enableClearValue && Ext.value(this.value, '') != '') {
            this.triggers[0].show();
        }

        if (this.fireEvent('beforecollapse', this) !== false) {
            this.list.hide();
            Ext.getDoc().un('mousewheel', this.collapseIf, this);
            Ext.getDoc().un('mousedown', this.collapseIf, this);
            this.fireEvent('collapse', this);
        }

    },
    expand: function() {
        if (this.isExpanded() || !this.hasFocus) {
            return;
        }
        if (this.fireEvent('beforeexpand', this) !== false) {

            this.list.alignTo.apply(this.list, [this.el].concat(this.listAlign));

            // zindex can change, re-check it and set it if necessary
            var listParent = Ext.getDom(this.getListParent() || Ext.getBody()),
                zindex = parseInt(Ext.fly(listParent).getStyle('z-index'), 10);
            if (!zindex) {
                zindex = this.getParentZIndex();
            }
            if (zindex) {
                this.list.setZIndex(zindex + 5);
            }

            this.triggers[0].hide();

            this.list.show(this.animate);

            if (Ext.isGecko2) {
                this.innerList.setOverflow('auto'); // necessary for FF 2.0/Mac
            }
            this.mon(Ext.getDoc(), {
                scope: this,
                mousewheel: this.collapseIf,
                mousedown: this.collapseIf
            });

            this.fireEvent('expand', this);
        }
    },
    collapseIf: function(e) {
        if (this.isExpanded() && !this.isDestroyed && !e.within(this.wrap) && !e.within(this.list)) {
            this.isTreeNodeClicked = true;
            this.collapse();
        }
    },
    onTriggerClick: function(e) {
        if (e.getTarget('#' + this.el.id, 1)) {
            return;
        }
        if (this.readOnly || this.disabled) {
            return;
        }
        if (this.isExpanded()) {
            this.collapse();
            this.el.focus();
        } else {
            this.onFocus({});
            this.expand();
            this.restrictHeight();
            this.el.focus();
        }
    },
    updateEditState: function() {
        if (this.rendered) {
            if (this.readOnly) {
                this.el.dom.readOnly = true;
                this.el.addClass('x-trigger-noedit');
                this.mun(this.el, 'click', this.onTriggerClick, this);
            } else {
                if (!this.editable) {
                    this.el.dom.readOnly = true;
                    this.el.addClass('x-trigger-noedit');
                    this.mon(this.el, 'click', this.onTriggerClick, this);
                } else {
                    this.el.dom.readOnly = false;
                    this.el.removeClass('x-trigger-noedit');
                    this.mun(this.el, 'click', this.onTriggerClick, this);
                }
                this.trigger.setDisplayed(!this.hideTrigger);
            }
            this.onResize(this.width || this.wrap.getWidth());
        }
    }
});
Ext.reg('xcomboboxtree', XG.Control.ComboBoxTree);

Ext.ns("XG.Form.SimpelPoupWin");
XG.Form.SimpelPoupWin = Ext.extend(Ext.Window, {
    constructor: function(config) {

        this.title = config.title;
        this.closable = true;
        this.closeAction = 'close';
        this.modal = true;
        this.constrain = true;
        //this.layout='fit';
        this.width = config.width;
        this.height = config.height;
        this.animateTarget = config.animateTarget;
        this.border = false;
        XG.Form.SimpelPoupWin.superclass.constructor.call(this, config);
    }
});
Ext.reg('poupwin', XG.Form.SimpelPoupWin);

Ext.ns("XG.Form.SimpelPoupForm");
XG.Form.SimpelPoupForm = Ext.extend(Ext.Window, {
    constructor: function(config) {
        this.submit_click = false;
        this.title = config.title;
        this.closable = true;
        this.closeAction = 'close';
        this.modal = true;
        this.constrain = true;
        //this.layout='fit';
        this.width = config.width;
        this.height = config.height;
        this.animateTarget = config.animateTarget;
        this.border = false;
        var win = this;
        var form = new Ext.FormPanel({
            bodyStyle: 'padding:5px 5px 0',
            region: 'center',
            fieldDefaults: {
                msgTarget: 'side'
            },
            collect_params: config.collect_params,
            labelWidth: config.labelWidth,
            defaultType: 'textfield',
            defaults: {
                allowBlank: false,
                width: config.fieldWidth
            },
            items: config.items,
            clear: function() {
                var form = win.items.itemAt(0).getForm();
                form.reset();
                var fields = form.items;
                for (var f in fields) {
                    if (fields[f].xtype == 'combobox') {
                        fields[f].setValue(fields[f].getStore().getAt(0));
                    }
                }
            },
            buttons: [{
                text: '保存',
                handler: function() {
                    var form = win.items.itemAt(0).getForm();
                    if (!form.isValid()) return;
                    var baseParams = {};
                    if (form.collect_params) {
                        var baseParams = form.collect_params(form);
                        if (!baseParams) return;
                    }
                    if (this.submit_click) return;
                    this.submit_click = true;
                    win.hide();
                    form.submit({
                        clientValidation: true,
                        url: config.url,
                        params: baseParams,
                        success: function(form, action) {
                            if (config.success) config.success();
                            if (action && action.hasOwnProperty('result') 
                                && action.result.hasOwnProperty('message') 
                                && action.result.message 
                                && action.result.message != "OK") {
                                alert(action.result.message);
                            }
                            win.close();
                        },
                        failure: function(form, action) {
                            if (config.failure) config.failure();
                            if (action && action.hasOwnProperty('result') 
                                && action.result.hasOwnProperty('message') 
                                && action.result.message) {
                                error(action.result.message);
                            } else {
                                error('发生异常！');
                            }
                            win.close();
                        }
                    });
                }
            }, {
                text: '取消',
                handler: function() {
                    var form = win.items.itemAt(0).getForm();
                    form.clear();
                    win.close();
                }
            }]
        });
        if (config.layout) {
            form.layout = config.layout;
            form.layoutConfig = config.layoutConfig;
        }
        config.layout = 'fit';
        config.items = [form];
        XG.Form.SimpelPoupForm.superclass.constructor.call(this, config);
    },
    fill: function(json) {
        form.reset();
        var filed, value;
        for (var obj in json) {
            fields = form.findField(obj);
            if (fields) {
                value = json[obj];
                if (true == value) {
                    value = 1;
                } else if (false == value) {
                    value = 0;
                }
                fields.setValue(value);
            }
        }
    }
});
Ext.reg('poupform', XG.Form.SimpelPoupForm);