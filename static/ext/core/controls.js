

Ext.ns("XG.Control.AbstractGrid");
XG.Control.AbstractGrid=Ext.extend(Ext.grid.GridPanel,{
    constructor:function(config){
        var itemsPerPage = 20;
        var stroe_fields = ['pk'];
        var columes=config.columes;
        var tbar=config.tbar;
        var baseParams=config.baseParams;
        var data_columes = [];
        if(config.id)this.id=config.id;
        if(!config.hasOwnProperty('nocheck'))
        {
            var sm=new Ext.grid.CheckboxSelectionModel({
                singleSelect:false,
                sortable:false
            });
            this.selModel=sm;
            data_columes.push(sm);  
        }

        var autoExpandColumn=null;
        for (var i=0;i<columes.length;i++) {
            stroe_fields.push(columes[i].dataIndex);
            if(columes[i].expend){
                autoExpandColumn=columes[i].id=Ext.id();
            }
            if (columes[i].hasOwnProperty('header')) {
                data_columes.push(columes[i]);
            }
        }


        var toolbar;
        if(isArrary(tbar)){
            toolbar=tbar;
        }
        else{
             toolbar=[];
             var control;
             for(var method in tbar){
                if(!(method in this))continue;
                if(isArrary(tbar[method])){
                    for(var i in tbar[method]){
                        control=this[method](tbar[method][i]);
                        toolbar.push(control);
                    }
                }else{
                    control=this[method](tbar[method]);
                    toolbar.push(control);
                }
            }
            if(tbar&&tbar.handlers)
            {
                for (var i = 0; i < tbar.handlers.length; i++) {
                   toolbar.push(tbar.handlers[i])
                }
            }
        }
        
        // var store = new Ext.data.JsonStore({
        //     totalProperty:'total',
        //     idProperty:'pk',
        //     fields:stroe_fields,
        //     root:'items',
        //     pageSize:itemsPerPage,
        //     proxy:new Ext.data.HttpProxy({
        //         type:'ajax',
        //         url:config.url
        //     })
        // });


        var store={
            xtype: 'jsonstore',
            totalProperty:'total',
            idProperty:'pk',
            fields:stroe_fields,
            pageSize:itemsPerPage,
            root:'items',
            url:config.url
        };
        if(baseParams){
            store.baseParams=baseParams;
        }
        config.store=store;
        this.stateful=true;
        this.multiSelect=true;
      //  this.store=store;
        this.cm=new Ext.grid.ColumnModel(data_columes);
        this.region='center';
        this.autoExpandColumn=autoExpandColumn;
        this.viewConfig={
            forceFit:true,
            stripeRows:true,
            enableTextSelection:true
        };
        if(!config.nopadding){
            config.bbar=new Ext.PagingToolbar({
                pageSize:itemsPerPage,
                store:store,
                displayInfo:true
            });
        }
        if(!config.notbar){
            config.tbar=toolbar;
        }
        XG.Control.AbstractGrid.superclass.constructor.call(this,config);

        this.getStore().load({
            params:{
                start:0,
                limit:itemsPerPage
            }
        });
    },
    getIdArr:function () {
        var record = Main.CurrentGrid().getSelectionModel().getSelections();
        var ids = [];
        if (!record||0==record.length) {
            alert('没有选中任数据!');
            return ids;
        }
        
        Ext.each(record, function (item) {
            ids.push(item.data.pk);
        });
        return ids;
    },
    getJsonArr:function(){
        return Main.CurrentGrid().getSelectionModel().getSelections();
    },
    getFirst:function () {
        var ids = Main.CurrentGrid().getIdArr();
        if (ids != null) {
            return ids[0];
        }
        return null;
    },
    del_row:function (config) {
        var iconCls = config.hasOwnProperty('iconCls') ? config.iconCls : 'Databasedelete';
        return {
            text:'删除选中',
            iconCls:iconCls,
            handler:function () {
                    var ids = Main.CurrentGrid().getIdArr();
                    if (!ids||ids.length==0)return;
                    confirm('确认删除选中的信息吗？<br/>相关联的数据也会被删除，请谨慎操作！', function (e) {
                        Ext.Ajax.request({
                            url:config.url,
                            method:"post",
                            params:{
                                ids:ids.join()
                            },
                            success:function () {
                                Main.CurrentGrid().getStore().load();
                                alert('删除成功!');
                            },
                            failure:function (form, action) {
                                if ('result' in action) {
                                    if ('msg' in action.result) {
                                        error(action.result.msg);
                                    }
                                }
                                else {
                                    error('发生异常!');
                                }
                            }
                        });
                    });
                }
            }
    },
    add_row:function(config){
        var iconCls = config.hasOwnProperty('iconCls') ? config.iconCls : 'Databaseadd';
        return {
            text:config.form.title,
            iconCls:iconCls,
            handler:function () {
                var form = XG.Form.AbstractForm.create(config.form);
                form.addListener('storereload', function () {
                    Main.CurrentGrid().getStore().load();
                    alert('添加成功！');
                });
                form.show(this);
            }
        };
    },
    update_row:function(config){
        var url = config.url;
        var iconCls = config.hasOwnProperty('iconCls') ? config.iconCls : 'Applicationedit';
        return {
            text:config.form.title,
            iconCls:iconCls,
            handler:function () {
                var form =XG.Form.AbstractForm.create(config.form);
                form.addListener('storereload', function () {
                    Main.CurrentGrid().getStore().load();
                    alert('修改成功！');
                });
                var sels = Main.CurrentGrid().getIdArr();
                if(sels.length!=1){
                    alert('请单选需要修改的数据！');
                    return;
                }
                var pk=sels[0];
                Ext.Ajax.request({
                    url:url,
                    method:"post",
                    params:{
                        id:pk
                    },
                    success:function (response) {
                        var json = Ext.util.JSON.decode(response.responseText);
                        form.form.fill(json);
                        form.show();
                    },
                    failure:function (form, action) {
                        if ('result' in action) {
                            if ('msg' in action.result) {
                                error(action.result.msg);
                            }
                        }
                        else {
                            error('发生异常!');
                        }
                    }
                });
            }
        };
    },
  
    modify_row:function(config){
        var text = config.text;
        var iconCls = config.hasOwnProperty('iconCls') ? config.iconCls : 'Vcardkey';
        return {
            text:config.form.title,
            iconCls:iconCls,
            handler:function () {
                var pk = Main.CurrentGrid().getFirst();
                if (pk == null)return;
                var form =XG.Form.AbstractForm.create(config.form);
                form.form.fill({'pk':pk});
                form.show();
            }
        };
    },
 
    
    approve_row:function(config){
        var win,form;
        return {
            text:config.title,
            iconCls:config.iconCls,
            handler:function (){
                var idArr = Main.CurrentGrid().getIdArr();
                if (null == idArr||0==idArr.length)return;
                var idsID=Ext.id();
                var passID=Ext.id();

                var argree=new Ext.Button({
                    text:config.argreeText?config.argreeText:"同意审核",
                    handler:function () {
                        var f=form.getForm();
                       
                        Ext.getCmp(idsID).setValue(idArr.join());
                        Ext.getCmp(passID).setValue(true);
                        if(config.agreeHandler){
                            config.agreeHandler(f,win);
                        }else{
                            if(!f.isValid())return;
                            f.submit({
                                url:config.url,
                                method:"post",
                                success:function () {
                                    win.close();
                                    Main.CurrentGrid().getStore().load();
                                    alert('操作成功!');
                                },
                                failure:function (form, action) {
                                    win.close();
                                    if ('result' in action) {
                                        if ('msg' in action.result) {
                                            error(action.result.msg);
                                        }
                                    }
                                    else {
                                        error('发生异常!');
                                    }

                                }
                            });
                        }
                    }
                });
                var disagree=new Ext.Button({
                    text:config.disagreeText?config.disagreeText:"退回请求", 
                    handler:function () {
                            var f=form.getForm();
                            Ext.getCmp(idsID).setValue(idArr.join());
                            Ext.getCmp(passID).setValue(false);
                            if(config.disagreeHandler){
                                config.disagreeHandler(f,win);
                            }else{
                                if(!f.isValid()) return;
                                f.submit({
                                    clientValidation: true,
                                    url: config.url,
                                    success:function () {
                                        win.close();
                                        Main.CurrentGrid().getStore().load();
                                        alert('审核成功!');
                                    },
                                    failure:function (form, action) {
                                        win.close();
                                        if ('result' in action) {
                                            if ('msg' in action.result) {
                                                error(action.result.msg);
                                            }
                                        }
                                        else {
                                            error('发生异常!');
                                        }
                                    }
                                });
                            }
                       
                        }
                    });
                var formItems=[];

                if(config.items){
                    for (var i = config.items.length - 1; i >= 0; i--) {
                        formItems.push(config.items[i]);
                    };
                }

                var optiontxt=config.optionText?config.optionText:"审核意见"
                var optionAllowBanlk=config.optionAllowBanlk?true:false;
                formItems.push({xtype:"textarea",fieldLabel:optiontxt,name:'option',width:200, height:80,allowBlank:optionAllowBanlk});
                formItems.push({xtype:"hidden",name:'ids',id:idsID});
                formItems.push({xtype:"hidden",name:'pass',id:passID});
                if(!config.width)config.width=350;
                if(!config.height)config.height=180;
                form = new Ext.FormPanel({
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
                    items:formItems,
                    clear: function() {
                        var form = win.items.itemAt(0).getForm();
                        form.reset();
                        var fields = form.items;
                        for(var f in fields) {
                            if(fields[f].xtype == 'combobox') {
                                fields[f].setValue(fields[f].getStore().getAt(0));
                            }
                        }
                    },
                    buttons: [argree,disagree]
                });
                win=new Ext.Window({
                    title:config.title,
                    closable:true,
                    closeAction:'close',
                    width:config.width,
                    minWidth:200,
                    height:config.height,
                    constrain:true,
                    layout:'fit',
                    modal:true,
                    items:[form]

                });
                win.show();
            }
        }
    },

    project_apply_type_combo:function(config){
        var p_types=config.p_types;
        chooice=[{pk:0,name:'显示所有类型'}];
        for(var i=0;i<p_types.length;i++){
            chooice.push(p_types[i]);
        }
        return {
            xtype:'combo',
            mode:'local',
            editable:false,
            valueField:'pk',
            displayField:   'name',
            triggerAction:  'all',
            forceSelection: true,
            name: 'prject_type',
            hiddenName:'project_type_id',
            anchor:'78%',
            value:0,
            store:new Ext.data.JsonStore({
                fields : ['pk','name'],
                data:chooice
            }),
            listeners:{
                select:function(combo,record,rowIdx){
                    var record = combo.getStore().getAt(rowIdx);
                    var pk=record.json.pk;
                    var gridStore=Main.CurrentGrid().getStore();
                    Ext.apply(  
                    gridStore.baseParams,  
                    {  
                        projecttype:pk
                    });
                    gridStore.load();
                }
            }
       };
    },
    choose_expert:function(config){
        var win;
        var submit={
            text:'确定',
            handler:function(){
                var expert_id=win.items.itemAt(1).getValue();
                var idArr = Main.CurrentGrid().getIdArr();
                win.close();
                Ext.Ajax.request({
                        url:'/expert/set/',
                        method:"post",
                        params:{
                            ids:idArr.join(),
                            expert_id:expert_id
                        },
                        success:function () {
                            win.close();
                            Main.CurrentGrid().getStore().load();
                            alert('设置成功!等待专家评审');
                        },
                        failure:function (form, action) {
                            win.close();
                            if ('result' in action) {
                                if ('msg' in action.result) {
                                    error(action.result.msg);
                                }
                            }
                            else {
                                error('发生异常!');
                            }
                        }
                    });
                }
        }
        
        return {
            text:'选择专家评审',
            iconCls:'Usercomment',
            handler:function(){
                var idArr = Main.CurrentGrid().getIdArr();
                if (null == idArr||0==idArr.length)return;
                win=new Ext.Window({
                    title:config.title,
                    closable:true,
                    closeAction:'close',
                    width:300,
                    minWidth:200,
                    height:100,
                    layout:{type:'absolute'},
                    modal:true,
                    items:[
                        {xtype:"label", text:"选择专家:", x:5, y:5},
                        {fieldLabel:'申报项目类型',name:'expert_id',url:'/expert/combo/',xtype:'remotecombo',x:65, y:5}
                    ],
                    buttons:[submit]
                });
                win.show();
            }
        }
    }
});
Ext.reg('basegrid',XG.Control.AbstractGrid);

Ext.ns("XG.Control.SexCombo");
XG.Control.SexCombo=Ext.extend(Ext.form.ComboBox,{
    initComponent: function() {
        Ext.apply(this,{
            hiddenName:'sex',
            store:new Ext.data.ArrayStore({
                fields:['text', 'value'],
                data:[['男', 1],['女', 0]]
            }),
            valueField:'value',
            displayField:'text',
            mode:'local',
            editable:false,
            triggerAction:'all',
            fieldLabel:'性别',
            width:180
        });  
        this.setValue(1);
    },
    fill:function(val){
        if(1==val||2==val){
            this.setValue(val);
        }
    }
});
Ext.reg('sexcombo',XG.Control.SexCombo);


Ext.ns("XG.Control.ProjectStatusCombo");
XG.Control.ProjectStatusCombo=Ext.extend(Ext.form.ComboBox,{
    initComponent: function() {
        Ext.apply(this,{
            triggerAction:'all',
            store:new Ext.data.ArrayStore({
                fields:['value', 'text'],
                data:[[1, '结项'],[0, '正常'],[-6, '延期'],[-5, '撤项']]
            }),
            valueField:'value',
            displayField:'text',
            mode:'local',
            editable:false,
            width:180
        });
        this.setValue(0);
    }
});
Ext.reg('proejctstatuscombo',XG.Control.ProjectStatusCombo);



Ext.ns("XG.Control.RemoteCombo");
XG.Control.RemoteCombo = Ext.extend(Ext.form.ComboBox,{
    constructor:function(config){
        this.name=config.name;
        this.url=config.url;
        this.baseParams=config.baseParams;
        this.valueField=config.valueField;
        this.displayField=config.displayField;
        XG.Control.RemoteCombo.superclass.constructor.call(this,config); 
    },
    initComponent: function() {
        var name=this.name,url=this.url;
        var valueField=this.valueField?this.valueField:'pk';
        var displayField=this.displayField?this.displayField:'name';
        var data=[];
        Ext.Ajax.request({
            url:url,
            async:false,
            success:function(response){
                var json=Ext.decode(response.responseText);
                var items=json.items;
                if(items||items.length>0){
                    for (var i = items.length - 1; i >= 0; i--) {
                        data.push([items[i][valueField],items[i][displayField]]);
                    };
                }
            }
        });
        data.reverse();
        this.data=data;
        var value=null;
        if(data.length>0){
            value=data[0][0];
        }
        Ext.apply(this,{
            hiddenName:name,
            store:new Ext.data.SimpleStore({
                fields:[valueField,displayField],
                data:data
            }),
            valueField:valueField,
            triggerAction:'all',
            displayField:displayField,
            mode:'local',
            editable:false,
            value:value
        });
    }

});
Ext.reg('remotecombo',XG.Control.RemoteCombo);


Ext.ns("XG.Control.LocalCombo");
XG.Control.LocalCombo = Ext.extend(Ext.form.ComboBox,{
    constructor:function(config){
        this.data=config.data;
        this.name=config.name;
        XG.Control.LocalCombo.superclass.constructor.call(this,config); 
    },
    initComponent: function() {
        var defaultValue,store;
        if(isArrary(this.data)){
            store=new Ext.data.SimpleStore({
                fields:['value','text'],
                data:this.data
            });
            defaultValue=this.data[0][0];
        }else{
            store=this.data;
            defaultValue=store.getAt(0).data.value;
        }
        Ext.apply(this,{
            hiddenName:this.name,
            name:this.name+'_s',
            store:store,
            valueField:'value',
            triggerAction:'all',
            displayField:'text',
            mode:'local',
            editable:false,
            value:defaultValue
        });
    },
    setValue:function(value){

        XG.Control.LocalCombo.superclass.setValue.call(this,value); 
    }
});
Ext.reg('localcombo',XG.Control.LocalCombo);


function DefaultCellHanlder(config){
    var handler=function(grid, rowIdx, colIdx, evt){
        if(colIdx==config.applyPdfIdx)//pdf
        {
            var record = grid.getStore().getAt(rowIdx);
            var pk=record.json.pk;
            window.open('/project/apply/pdf/download/'+pk+'/');
        }
        else if(colIdx==config.pdfIdx)
        {
            var record = grid.getStore().getAt(rowIdx);
            var pk=record.json.document_id;
            window.open('/document/download/'+pk+'/');
        }
        else if(colIdx==config.applyIdx)
        {
            var record = grid.getStore().getAt(rowIdx);
            var pk=record.json.pk;
            var win=new Ext.Window({
                    title:'项目申请详情',
                    closable:true,
                    closeAction:'close',
                    width:600,
                    minWidth:400,
                    height:400,
                    layout:{type:'absolute'},
                    modal:true,
                    autoLoad:{
                        url:'/project/apply/showdetails/',
                        params:{
                            pk:pk
                        },
                        text: "正在读取...",
                        timeout: 20,
                        scripts: false 
                    },
                    buttons:[{
                        text:'关闭',
                        handler:function(){
                            win.close();
                        }
                    }]
            });
            win.show();
        }
        else if(colIdx==config.projectIdx)
        {
            var record = grid.getStore().getAt(rowIdx);
            var pk=record.json.pk;
            var win=new Ext.Window({
                    title:'项目详情',
                    closable:true,
                    closeAction:'close',
                    width:600,
                    minWidth:400,
                    height:400,
                    layout:{type:'absolute'},
                    modal:true,
                    autoLoad:{
                        url:'/project/show/details/',
                        params:{
                            pk:pk
                        },
                        text: "正在读取...",
                        timeout: 20,
                        scripts: false 
                    },
                    buttons:[{
                        text:'关闭',
                        handler:function(){
                            win.close();
                        }
                    }]
            });
            win.show();
        }
        else if(colIdx==config.userIdx)
        {
            
        }
        else if(colIdx==config.messageIdx)
        {
            var record = grid.getStore().getAt(rowIdx);
            var pk=record.json.pk;
            var win=new Ext.Window({
                    title:'消息内容',
                    closable:true,
                    closeAction:'close',
                    width:600,
                    minWidth:400,
                    height:400,
                    layout:{type:'absolute'},
                    modal:true,
                    autoLoad:{
                        url:'/message/show/details/',
                        params:{
                            pk:pk
                        },
                        text: "正在读取...",
                        timeout: 20,
                        scripts: false 
                    },
                    buttons:[{
                        text:'关闭',
                        handler:function(){
                            win.close();
                        }
                    }]
            });
            win.show();
        }
        else if(colIdx==config.showExpertIdx)
        {
            var record = grid.getStore().getAt(rowIdx);
            var pk=record.json.pk;
            function YesNo(value){
                return value==1?'是':'否';
            }
            var win=new Ext.Window({
                title:'专家评分',
                width:700,
                minWidth:400,
                height:400,
                layout:'fit',
                items:[{
                    xtype:'basegrid',
                    url:'/project/apply/expertapproves/',
                    nocheck:true,
                    baseParams:{
                        pk:pk
                    },
                    columes:[
                        {header:'项目名称', dataIndex:'apply__project_name', flex:1 },
                        {header:'项目编号', dataIndex:'apply__project_no', flex:1 },
                        {header:'评审专家', dataIndex:'expert__name', flex:1 },
                        {header:'拒绝评审', dataIndex:'refused', flex:1,renderer:YesNo},
                        {header:'评审时间', dataIndex:'approvetime', flex:1,
                            renderer:function(value, cellmeta, record, rowIndex, columnIndex, store){
                                return record.data['approved']?value:'';
                            }
                        },
                    
                        {header:'评分', dataIndex:'expert_percent', flex:1 },
                        {header:'资助意见', dataIndex:'expert_support', flex:1 },
                        {header:'邮件回执', dataIndex:'email_back', flex:1,renderer:YesNo}
                    ]   
                }]
            });
            win.show();
        }
    }
    return handler;
}


function DefaultDateFeild(config){
    if(!config)config={};
    config.xtype='datefield'; 
    config.editable=false;
    config.altFormats='Y年m月d日'; 
    config.format='Y年m月d日';
    config.allowBlank=false;
    if(!config.anchor)config.anchor='78%';
    return config;
}

Ext.ns("XG.Render.UnitLevel");
/**
 * @return {string}
 */
XG.Render.UnitLevel = function (value) {
    switch (value) {
        case 0:
            return '国家民委';
        case 1:
            return '一级单位';
        case 2:
            return '二级单位';
        case 3:
            return '三级单位';
        case 4:
            return '四级单位';
        case 5:
            return '五级单位';
        case 6:
            return '六级单位';
        case 7:
            return '七级单位';
        case 8:
            return '八级单位';
        default:
            return '未知'
    }
};


Ext.ns("XG.Render.ProjectStatus");
/**
 * @return {string}
 */
XG.Render.ProjectStatus = function (value) {
    switch (value) {
        case -7:
            return '退回';
        case -6:
            return '延期';
        case -5:
            return '撤项';
        case 0:
            return '立项';
        case 1:
            return '结项';
        default:
            return 'unknown';
    }
};


Ext.ns("XG.Render.ApproveStatus");
/**
 * @return {string}
 */
XG.Render.ApproveStatus = function (value) {
    switch (value) {
        case -9:
            return '等待提交';
        case -8:
            return '国家民委管理员退回';
        case -6:
            return '二级单位管理员退回';
        case -7:
            return '一级单位管理员退回';
        case -5:
            return '等待推送专家评审';
        case -4:
            return '待项目主管部门审核';
        case -3:
            return '等待专家评审';
        case -2:
            return '等待二级管理员审核';
        case -1:
            return '等待一级管理员审核';
        case -10:
            return '待项目主管部门审查';
        case 1:
            return '立项';
        case 0:
            return '失败';
        default:
            return 'unknown';
    }
};



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
        this.sbId=Ext.id();
        var form = new Ext.FormPanel({
            bodyStyle: 'padding:5px 5px 0',
            region: 'center',
            fieldDefaults: {
                msgTarget: 'side'
            },
            autoScroll:true,
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
                for(var f in fields) {
                    if(fields[f].xtype == 'combobox') {
                        fields[f].setValue(fields[f].getStore().getAt(0));
                    }
                }
            },
            buttons: [{
                text: '保存',
                id:win.sbId,
                handler: function() {
                    var form = win.items.itemAt(0).getForm();
                    if(!form.isValid()) return;
                    if(config.vailidate)
                    {
                        if(!config.vailidate(form))
                        {
                            return;
                        }
                    }
                    var baseParams = {};
                    if(form.collect_params) {
                        var baseParams = form.collect_params(form);
                        if(!baseParams) return;
                    }
                    if(this.submit_click) return;
                    this.submit_click = true;
                    win.hide();
                    form.submit({
                        clientValidation: true,
                        url: config.url,
                        params: baseParams,
                        success: function(form, action) {
                            if(config.success) config.success();
                            else if(action && action.hasOwnProperty('result') && action.result.hasOwnProperty('message') && action.result.message && action.result.message != "OK") {
                                alert(action.result.message);
                            }
                            win.close();
                        },
                        failure: function(form, action) {
                            if(config.failure) config.failure();
                            else if(action && action.hasOwnProperty('result') && action.result.hasOwnProperty('message') && action.result.message) {
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
        
        if(config.layout) {
            form.layout = config.layout;
            form.layoutConfig = config.layoutConfig;
        }
        config.layout = 'fit';
        config.items = [form];

  
        XG.Form.SimpelPoupForm.superclass.constructor.call(this, config);
    },
    setReadOnly:function(bReadOnly){
        var items=this.getItems();
        for (var i = items.length - 1; i >= 0; i--) {
            if(items[i].setReadOnly){
                items[i].setReadOnly(true);
            }
        };
        Ext.getCmp(this.sbId).hide();
    },
    getItems:function(){
        var form=this.items.itemAt(0).getForm();
        var items=[];
        form.items.each(function (field) {
            if(items.xtype=='fieldset'){
                items.items.each(function(f){
                    items.pushp[f];
                });
            }else if(items.xtype=='onetomanyfields'){
                var temp=[];
                items.items.each(function(f){
                    temp.pushp[f];
                });
            }else{
                items.push(field);
            }
        });
        return items;
    },
    fill:function (json) {
        var form=this.items.itemAt(0).getForm();
        var filed,value;
        var one2manys=this.find('xtype','onetomanyfields');
        for(var obj in json){
            if(isArrary(json[obj])){
                var jarray=json[obj];
                var gfield=null;
                if(!one2manys||one2manys.length==0)continue;
                for (var i = one2manys.length - 1; i >= 0; i--) {
                    gfield=one2manys[i];
                    if(!gfield.gname!=obj)continue;
                    break;
                };
                if(!gfield)continue;
                gfield.setValue(jarray);
            }else{
                fields=form.findField(obj);
                if(fields){
                    value = json[obj];
                    if(true==value){
                        value=1;
                    }
                    else if(false==value){
                        value=0;    
                    }
                    fields.setValue(value);
                }
            }
        }
            
    }
});
Ext.reg('poupform', XG.Form.SimpelPoupForm);


Ext.ns("XG.UserFields");
XG.UserFields = {
    pk:{name:'pk', inputType:'hidden'},
    regname:{fieldLabel:'用户名', name:'name',vtype:'username'},
    name:{fieldLabel:'用户名', name:'name'},
    password:{ fieldLabel:'密码', name:'password', inputType:'password'},
    real_name:{fieldLabel:'真实姓名', name:'real_name'},
    sex:{fieldLabel:'性别',xtype:'sexcombo'},
    unit_name:{fieldLabel:'单位名称', name:'unit_name'},
    unit_id:{fieldLabel:'所在单位',name:'unit_id',url:'/unit/combo/',xtype:'remotecombo'},
    role_id:{fieldLabel:'用户角色',name:'role_id',url:'/role/combo/',xtype:'remotecombo'},
    phone:{fieldLabel:'电话', name:'phone'},
    mobile:{fieldLabel:'手机', name:'mobile'},
    remark:{xtype:'textarea', fieldLabel:'备注', name:'remark'},
    email:{fieldLabel: 'Email',name: 'email',vtype:'email'},
    study_type_name:{fieldLabel:'学科编号', name:'study_type_name'}
};


Ext.ns("XG.UnitFields");
XG.UnitFields = {
    pk:{name:'pk', inputType:'hidden'},
    name:{fieldLabel:'单位名称', name:'name'},
    parent_unit_id:{fieldLabel:'所属单位名称',name:'parent_unit_id',url:'/unit/combo/',xtype:'remotecombo'},
    project_type_id:
    {
        fieldLabel:'申报项目类型',
        name:'project_type_id',
        allowBlank:false,
        xtype:'superboxselect',
        emptyText: '选择项目类型',
        resizable: true,
        minChars: 2,
        store:{
            xtype: 'jsonstore',
            totalProperty:'total',
            idProperty:'pk',
            fields:['pk','name'],
            root:'items',
            url:'/projecttype/combo/'
        },
        mode: 'remote',
        displayField: 'name',
        valueField: 'pk',
        queryDelay: 0,
        triggerAction: 'all'
    },
    no:{fieldLabel:'单位名称全拼', name:'no',emptyText:'(每个字首字母大写)'},
    parent_unit__name:{fieldLabel:'所属单位名称', name:'parent_unit__name'},
    phone:{fieldLabel:'电话', name:'phone'},
    address:{fieldLabel:'单位地址', name:'address'},
    max_project:{name:'max_project', fieldLabel:'最大申请项目数'},
    apply_starttime:{name:'apply_starttime', fieldLabel:'申报开始时间', xtype:'datefield', altFormats:'Y年m月d日', format:'Y年m月d日',width:170},
    apply_endtime:{name:'apply_endtime', fieldLabel:'申报结束时间', xtype:'datefield', altFormats:'Y年m月d日', format:'Y年m月d日',width:170}
};

Ext.ns("XG.ProjectTypeFields");
XG.ProjectTypeFields = {
    pk:{name:'pk', inputType:'hidden'},
    name:{fieldLabel:'项目类型名称', name:'name'},
    waring_day:{fieldLabel:'项目预警天数', name:'waring_day'},
    allow_apply:{fieldLabel:'允许申报',xtype:'checkbox',name:'allow_apply'},
    max_project_num:{fieldLabel:'最大申请项目数', name:'max_project_num'}
};

Ext.ns("XG.ProjectFields");
XG.ProjectFields = {
    pk:{name:'pk', inputType:'hidden'},
    name:{fieldLabel:'项目名称', name:'name'},
    no:{fieldLabel:'项目编号', name:'no'},
    status:{fieldLabel:'项目状态', name:'status'},
    applicant_opinion:{fieldLabel:'项目说明', name:'applicant_opinion', xtype:"textarea",height:80},
    project_type_id:{fieldLabel:'项目类型',name:'project_type_id',url:'/projecttype/combo/',xtype:'remotecombo'}
};

Ext.ns("XG.ProjectExChangeFields");
XG.ProjectExChangeFields = {
    pk:{name:'pk', inputType:'hidden'},
    forward_status:{xtype:'proejctstatuscombo',fieldLabel:'项目变更类型',hiddenName:'forward_status'},
    applicant_opinion:{fieldLabel:'项目说明', name:'applicant_opinion',xtype:"textarea", height:80}

};

Ext.ns("XG.Message");
XG.Message={
    receiver_unit_id:{fieldLabel:'公告接收单位',name:'receiver_unit_id',url:'/unit/combo',xtype:'remotecombo'},
    title:{fieldLabel:'项目名称', name:'title'},
    abstract:{fieldLabel:'项目名称', name:'abstract'},
    content:{fieldLabel:'项目名称', name:'content'}
}

Ext.ns("XG.Form.OneToManyFields");
XG.Form.OneToManyFields=Ext.extend(Ext.form.FieldSet ,{
    constructor: function(config) {
        var id=config.id?config.id:Ext.id();
        var gname=config.gname;
        this.id=id;
        var items=[],curitem,json;
        var me=this;
        this.border=true;
        this.store=[];
        if(config.collapsible)this.collapsible=true;
        for (var i = config.citems.length - 1; i >= 0; i--) {
            var curitem=config.citems[i];
            if(curitem.xtype=='groupcombo'){
                var data=[];
                Ext.Ajax.request({
                    url:curitem.url,
                    async:false,
                    success:function(response){
                        json=Ext.decode(response.responseText);
                        for (var i = json.items.length - 1; i >= 0; i--) {
                            data.push([
                                json.items[i][curitem.valueField],
                                json.items[i][curitem.displayField]]);
                        };
                    }
                });
                data.reverse();
                this.store[curitem.name]=new Ext.data.SimpleStore({
                    fields:['value','text'],
                    data:data
                });
                items.push({
                    fieldLabel:curitem.fieldLabel,
                    xtype:'localcombo',
                    name:curitem.name,
                    data:this.store[curitem.name],
                    listeners:curitem.listeners
                });
            }else{
                items.push(curitem);
            }
        };
        items.reverse();

        this.addSelf=function(){
            var f=Ext.getCmp(id);
            if(config.max){
                var index=f.items.length;
                if(index>=config.max){
                    alert('限填'+config.max+'项,无法继续添加信息了！');
                    return;
                }
            }    
            f.add({
                xtype:'fieldset',
                bodyStyle:'padding:5px',
                items:items
            });
            f.doLayout()
        }

        this.removeSelf=function(){
            var f=Ext.getCmp(id);
            var index=f.items.length;
            if(index<=1)return;
            var cmp=f.items.items[index-1];
            f.remove(cmp,true);
        }

        this.setValue=function(jarray){
            var f=Ext.getCmp(id);
            var len=jarray.length-1,fields,filedName;
            for (var i = len - 1; i >= 0; i--)f.addSelf();
            for(var attr in jarray[0]){
                filedName='g__'+gname+'__'+attr;
                fields=f.find('name',filedName);
                //combo hiddname
                if(!fields||fields.length==0)fields=f.find('name',filedName+'_s');
                if(!fields||fields.length==0)continue;
                for (var i = fields.length - 1; i >= 0; i--) {
                    fields[i].setValue(jarray[i][attr]);
                };
            }
        }

        this.refreshStore=function(fieldName){

        }

        this.getStore=function(fieldName){
            return me.store[fieldName]
        }

        this.setReadOnly=function(bReadOnly){
            var f=Ext.getCmp(id);
            for (var i = 0; i < f.buttons.length; i++) {
                if(bReadOnly){
                    f.buttons[i].hide();
                }else{
                    f.buttons[i].show();
                }
            };
        }

        this.buttons=[
            {
                text:'继续添加',
                handler:this.addSelf
            },
            {
                text:'移除',
                handler:this.removeSelf
            }
        ];
        this.config=config;
        this.items=[{
            xtype:'fieldset',
            bodyStyle:'padding:5px',
            items:items
        }];
        XG.Form.OneToManyFields.superclass.constructor.call(this, config);
    }

});
Ext.reg('onetomanyfields',XG.Form.OneToManyFields);


Ext.ns("XG.Form.AbstractForm");
XG.Form.AbstractForm.create = function (config) {
    var submit_click=false;
    var submit = new Ext.Button({
        text:'保存',
        handler:function () {
            if (!form.isValid())return;
            if(submit_click)return;
            if(config.vailidate)
            {
                if(!config.vailidate(form))
                {
                    return;
                }
            }
            submit_click=true;
            win.hide();
            form.submit({
                clientValidation:true,
                url:config.url,
                success:function (form, action) {
                    if (action.result.msg != 'OK') {
                        alert(action.result.msg);
                    }
                    form.reset();
                    win.fireEvent('storereload');
                    win.close();
                },
                failure:function (form, action) {
                    if (action
                        && action.hasOwnProperty('result')
                        && action.result.hasOwnProperty('msg')
                        && action.result.msg) {
                        error(action.result.msg);
                    }
                    else {
                        error('发生异常！');
                    }
                    form.reset();
                    win.close();
                }
            });
        }
    });
    var cancel = new Ext.Button({
        text:'取消',
        handler:function () {
            formPanel.clear();
            win.close();
        }
    });

    var formPanel = new Ext.FormPanel({
        bodyStyle:'padding:5px 5px 0',
        region:'center',
        autoScroll:true,
        fieldDefaults:{
            msgTarget:'side'
        },
        labelWidth:90,
        defaultType:'textfield',
        defaults:{
            allowBlank:false,
            width:230
        },
        items:config.items,
        clear:function () {
            form.reset();
            var fields = form.items;
            for (var f in fields) {
                if (fields[f].xtype == 'combobox') {
                    fields[f].setValue(fields[f].getStore().getAt(0));
                }
            }
        },
        fill:function (json) {
            form.reset();
            var filed,value;
            var one2manys=formPanel.find('xtype','onetomanyfields');
            for(var obj in json){
                if(isArrary(json[obj])){
                    var jarray=json[obj];
                    var gfield=null;
                    if(!one2manys||one2manys.length==0)continue;
                    for (var i = one2manys.length - 1; i >= 0; i--) {
                        gfield=one2manys[i];
                        if(!gfield.gname!=obj)continue;
                        break;
                    };
                    if(!gfield)continue;
                    gfield.setValue(jarray);
                }else{
                    fields=form.findField(obj);
                    if(fields){
                        value = json[obj];
                        if(true==value){
                            value=1;
                        }
                        else if(false==value){
                            value=0;    
                        }
                        fields.setValue(value);
                    }
                }
            }
        },
        buttons:[submit, cancel]
    });
    var form = formPanel.getForm();
    var win = new Ext.Window({
        title:config.title,
        form:formPanel,
        closable:true,
        closeAction:'close',
        modal:true,
        width:config.width,
        height:config.height,
        layout:{
            type:'border',
            padding:5
        },
        items:[formPanel]
    });
    return win;
};

Ext.ns("XG.Form.MessageForm");
XG.Form.MessageForm.create = function (config) {
    var submit_click=false;
    var submit = new Ext.Button({
        text:'保存',
        handler:function () {
            if (!form.isValid())return;
            if(submit_click)return;
            submit_click=true;
            win.hide();
            form.submit({
                clientValidation:true,
                url:config.url,
                success:function (form, action) {
                    if (action.result.msg != 'OK') {
                        alert(action.result.msg);
                    }
                    form.reset();
                    win.fireEvent('storereload');
                    win.close();
                },
                failure:function (form, action) {
                    if (action
                        && action.hasOwnProperty('result')
                        && action.result.hasOwnProperty('msg')
                        && action.result.msg) {
                        error(action.result.msg);
                    }
                    else {
                        error('发生异常！');
                    }
                    form.reset();
                    win.close();
                }
            });
        }
    });
    var cancel = new Ext.Button({
        text:'取消',
        handler:function () {
            formPanel.clear();
            win.close();
        }
    });

    var formPanel = new Ext.FormPanel({
        frame:true,
        bodyStyle:'padding:5px 5px 0',
        region:'center',
        fieldDefaults:{
            msgTarget:'side'
        },
        labelWidth:90,
        defaultType:'textfield',
        defaults:{
            allowBlank:false,
            width:230
        },
        items:config.items,
        clear:function () {
            form.reset();
            var fields = form.items;
            for (var f in fields) {
                if (fields[f].xtype == 'combobox') {
                    fields[f].setValue(fields[f].getStore().getAt(0));
                }
            }
        },
        fill:function (json) {
            form.reset();
            var filed,value;
            for(var obj in json){
                fields=form.findField(obj);
                if(fields){
                    value = json[obj];
                    if(true==value){
                        value=1;
                    }
                    else if(false==value){
                        value=0;    
                    }
                    fields.setValue(value);
                }
            }
        },
        buttons:[submit, cancel]
    });
};

