var AjaxFilter=function(conn, response, options){  
    var s = response.responseText;
    if(response.status=="905"){  
        Ext.Msg.alert('提示', '会话超时，请重新登录!', function(){  
            window.location.href = '/login.html';    
        });      
    }        
    else if(s.indexOf("TRACE:",0) ==0){
        var win=new Ext.Window({
            title : '错误信息-该信息仅在在调试时显示',
            closable : true,
            closeAction : 'close',
            modal : true,
            constrain : true,
            layout:'fit',
            width : 800,
            height : 600,
            border : false,
            html:Ext.encode(s)
        });
        win.show();
    }  
};

Ext.Ajax.on('requestcomplete',AjaxFilter);
Ext.Ajax.on('requestexception',AjaxFilter);  



function alert(msg){Ext.Msg.alert('提示',msg);}
function warning(msg){Ext.Msg.alert('警告',msg);}
function error(msg){Ext.Msg.alert('错误',msg);}
function confirm(msg,fun){
    Ext.Msg.confirm('警告',msg,function(e){
        if(e=='yes'){
            fun(e);
        }
    });
}

function fileExt(value){
    return /\.[^\.]+$/.exec(form.items.items[0].value);
}

function encodehtml(value){
    return Ext.util.Format.htmlEncode(value);
}

function decodehtml(value){
    return Ext.util.Format.htmlDecode(value);
}

function debugform(form){
    var s ='';   
    Ext.iterate(form.form.getValues(), function(key, value) {
        s += String.format("{0} = {1}<br />", key, value);
    }, this);
    alert(s);  
}

function falsefunc(){
    return false;
}

function mask(msg){
    Ext.getBody().mask(msg);  
}
function unmask(){
    Ext.getBody().unmask();
}

function isArrary(obj){
    return Object.prototype.toString.call(obj) === '[object Array]';      
}

function fileExt(value){
    var ext= /\.[^\.]+$/.exec(value);
    if(!ext)return "";
    if(isArrary(ext)&&ext.length>0)ext=ext[0];
    if(ext.length>1) ext=ext.substring(1);
    return ext;
}

function dateDiff(n) 
{ 
    var beginDate = new Date();  
    beginDate.setDate(beginDate.getDate()+n);
    return beginDate; 
} 

function existFile(name,path,func)
{
    Ext.Ajax.request({  
        url:'/logic/DocFileInfoHandler.ashx?f=FileExists',
        async:false,
        params:{
            path:path
        },
        method:'post',  
        success:function(response,options){ 
            var res = Ext.util.JSON.decode(response.responseText);
            res.name=name;
            if(res.success)
            {
                func(res);
            }
            else{
                error('指定的文件路径不存在！');
            }
        }
    });
}

function downloadFile(json,fileInfoID){
    existFile(json.Name,json.FtpPath,function(res){
        var elemIF = document.createElement("iframe");
        var url='/logic/DocFileInfoHandler.ashx?f=FileDownLoad';
        url+='&name='+json.Name;
        url+='&path='+json.FtpPath;
        url+="&fid="+fileInfoID;
        if(json.AuthCode)url+='&code='+json.AuthCode;
        if(json.LimitTime)url+='&time='+json.LimitTime;
        elemIF.src =url;
        elemIF.style.display = "none";
        document.body.appendChild(elemIF);
    });
}

function isSupportView(ext){
    if('.doc.xls.ppt.docx.xlsx.pptx.wps.dps.et.pdf.jpg.png.bmp.gif.txt.cs.py.ini'.indexOf(ext)<0){
        return false;
    }
    return true;
}

function ShowDocumentViewWin(fileName,ftpPath){
    var ext=fileExt(fileName);
    if(!isSupportView(ext)){
        alert('不支持'+ext+'文件格式预览');
        return;
    }
    var documentViewWin = new XG.Form.SimpelPoupWin({
        width: 800,
        height: 630,
        layout: 'fit',
        title: String.format('{0} --- 预览',fileName),
        resizable: false,
        html:String.format('<iframe name="frame" src="/DocumentView.aspx?ftpPath={0}" width="100%" height="100%"/>',ftpPath)
    });
    documentViewWin.show();
};


Ext.apply(Ext.form.VTypes, {
    daterange : function(val, field) {
        var date = field.parseDate(val);
        if(!date){
            return false;
        }
        if (field.startDateField) {
            var start = Ext.getCmp(field.startDateField);
            if (!start.maxValue || (date.getTime() != start.maxValue.getTime())) {
                start.setMaxValue(date);
                start.validate();
            }
        }
        else if (field.endDateField) {
            var end = Ext.getCmp(field.endDateField);
            if (!end.minValue || (date.getTime() != end.minValue.getTime())) {
                end.setMinValue(date);
                end.validate();
            }
        }
        return true;
    },
    password : function(val, field) {
        // if (field.initialPassField) {
        //     var pwd = Ext.getCmp(field.initialPassField);
        //     return (val == pwd.getValue());
        // }
        return true;
    },
    passwordText : '两次输入密码不一致',
    username:function(val,field){
        if(field.lastname==val)return true;
        var result;   
        Ext.Ajax.request({  
            url:'/user/name/',
            async:false,
            params:{
                name:val
            },
            method:'post',  
            success:function(response,options){  
                var res = Ext.util.JSON.decode(response.responseText);  
                if(res.msg=='OK'){
                    result=true;
                    field.lastname=val;
                    field.clearInvalid();
                }else{
                    result=false;
                }
            }
        });
        return result;
    },
    usernameText:'用户名已经存在',

    positive:function(val,field){
        try  
        {  
            if(/^[1-9][\d]*$/.test(val))  
                return true;  
            return false;  
        }  
        catch(e)  
        {  
            return false;  
        }  
    },

    positiveText:'请输入正确的正整数！',

    future_date:function(val,field){
        try  
        {   
            return field.getValue()>new Date()
        }  
        catch(e)  
        {  
            return false;  
        }  
    },
    future_dateText:'必须大于当前时间！'
});

Ext.namespace("Ext.ux");
Ext.ux.NotificationMgr = {
    positions: []
};

//右下角弹出
Ext.ux.Notification = Ext.extend(Ext.Window, {
    constructor:function(config){
       Ext.Window.superclass.constructor.call(this,config); 
    },
    initComponent: function(){
        Ext.apply(this, {
            iconCls: this.iconCls || 'x-icon-information',
            cls: 'x-notification',
           
            plain: false,
            draggable: false,
            bodyStyle: 'text-align:left'
        });
        if(this.autoDestroy) {
            this.task = new Ext.util.DelayedTask(this.hide, this);
        } else {
            this.closable = true;
        }
        Ext.ux.Notification.superclass.initComponent.call(this);
    },
    setMessage: function(msg){
        this.body.update(msg);
    },
    setTitle: function(title, iconCls){
        Ext.ux.Notification.superclass.setTitle.call(this, title, iconCls||this.iconCls);
    },
    onRender:function(ct, position) {
        Ext.ux.Notification.superclass.onRender.call(this, ct, position);
    },
    onDestroy: function(){
        Ext.ux.NotificationMgr.positions.remove(this.pos);
        Ext.ux.Notification.superclass.onDestroy.call(this);
    },
    cancelHiding: function(){
        this.addClass('fixed');
        if(this.autoDestroy) {
            this.task.cancel();
        }
    },
    afterShow: function(){
        Ext.ux.Notification.superclass.afterShow.call(this);
        Ext.fly(this.body.dom).on('click', this.cancelHiding, this);
        if(this.autoDestroy) {
            this.task.delay(this.hideDelay || 5000);
       }
    },
    animShow: function(){
        this.pos = 0;
        while(Ext.ux.NotificationMgr.positions.indexOf(this.pos)>-1)
            this.pos++;
        Ext.ux.NotificationMgr.positions.push(this.pos);
        this.setSize(this.width,this.height);
        this.el.alignTo(document, "br-br", [ -20, -20-((this.getSize().height+10)*this.pos) ]);
        this.el.slideIn('b', {
            duration: 1,
            callback: this.afterShow,
            scope: this
        });
    },
    animHide: function(){
        Ext.ux.NotificationMgr.positions.remove(this.pos);
        this.el.ghost("b", {
            duration: 1,
            remove: true
        });
    },
    focus: Ext.emptyFn 
}); 
//tab 右键目录
Ext.ux.TabCloseMenu = Ext.extend(Object, {
    closeTabText: '关闭标签',
    closeOtherTabsText: '除此以外全部关闭',
    showCloseAll: true,
    closeAllTabsText: '关闭全部标签',
    constructor : function(config){
        Ext.apply(this, config || {});
    },
    //public
    init : function(tabs){
        this.tabs = tabs;
        tabs.on({
            scope: this,
            contextmenu: this.onContextMenu,
            destroy: this.destroy
        });
    },
    destroy : function(){
        Ext.destroy(this.menu);
        delete this.menu;
        delete this.tabs;
        delete this.active;    
    },
    // private
    onContextMenu : function(tabs, item, e){
        this.active = item;
        var m = this.createMenu(),
            disableAll = true,
            disableOthers = true,
            closeAll = m.getComponent('closeall');
        
        m.getComponent('close').setDisabled(!item.closable);
        tabs.items.each(function(){
            if(this.closable){
                disableAll = false;
                if(this != item){
                    disableOthers = false;
                    return false;
                }
            }
        });
        m.getComponent('closeothers').setDisabled(disableOthers);
        if(closeAll){
            closeAll.setDisabled(disableAll);
        }
        
        e.stopEvent();
        m.showAt(e.getPoint());
    },
    createMenu : function(){
        if(!this.menu){
            var items = [{
                itemId: 'close',
                text: this.closeTabText,
                scope: this,
                handler: this.onClose
            }];
            if(this.showCloseAll){
                items.push('-');
            }
            items.push({
                itemId: 'closeothers',
                text: this.closeOtherTabsText,
                scope: this,
                handler: this.onCloseOthers
            });
            if(this.showCloseAll){
                items.push({
                    itemId: 'closeall',
                    text: this.closeAllTabsText,
                    scope: this,
                    handler: this.onCloseAll
                });
            }
            this.menu = new Ext.menu.Menu({
                items: items
            });
        }
        return this.menu;
    },
    onClose : function(){
        this.tabs.remove(this.active);
    },
    onCloseOthers : function(){
        this.doClose(true);
    },
    onCloseAll : function(){
        this.doClose(false);
    },
    doClose : function(excludeActive){
        var items = [];
        this.tabs.items.each(function(item){
            if(item.closable){
                if(!excludeActive || item != this.active){
                    items.push(item);
                }    
            }
        }, this);
        Ext.each(items, function(item){
            this.tabs.remove(item);
        }, this);
    }
});
Ext.preg('tabclosemenu', Ext.ux.TabCloseMenu);


function JPost(config){
    if(config.async!=false)config.async=true;
    Ext.Ajax.request({
        url:config.url,
        method:"post",
        async:config.async,
        params:config.params,
        success:function (response,options) {
            var res = Ext.util.JSON.decode(response.responseText);
            if(res.message=="OK")return;
            if(config.alert&&res.message){
                if(res.success){
                    alert(res.message);
                }else{
                    error(res.message);
                }
            }
            config.success(res);
        },
        failure:function (form, action) {
            if(config.errorText){
                error(config.errorText);
                return;
            }
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

Ext.lib.Ajax.defaultPostHeader += ";charset=utf-8";
Ext.ns('Ext.ux.form');
Ext.ux.form.FileUploadField = Ext.extend(Ext.form.TextField,  {
    buttonText: '选择文件...',
    buttonOnly: false,
    buttonOffset: 3,
    readOnly: true,
    autoSize: Ext.emptyFn,
    initComponent: function(){
        Ext.ux.form.FileUploadField.superclass.initComponent.call(this);
        this.addEvents(
            'fileselected'
        );
    },
    // private
    onRender : function(ct, position){
        Ext.ux.form.FileUploadField.superclass.onRender.call(this, ct, position);
        this.wrap = this.el.wrap({cls:'x-form-field-wrap x-form-file-wrap'});
        this.el.addClass('x-form-file-text');
        this.el.dom.removeAttribute('name');
        this.createFileInput();

        var btnCfg = Ext.applyIf(this.buttonCfg || {}, {
            text: this.buttonText
        });
        this.button = new Ext.Button(Ext.apply(btnCfg, {
            renderTo: this.wrap,
            cls: 'x-form-file-btn' + (btnCfg.iconCls ? ' x-btn-icon' : '')
        }));

        if(this.buttonOnly){
            this.el.hide();
            this.wrap.setWidth(this.button.getEl().getWidth());
        }

        this.bindListeners();
        this.resizeEl = this.positionEl = this.wrap;
    },
    bindListeners: function(){
        this.fileInput.on({
            scope: this,
            mouseenter: function() {
                this.button.addClass(['x-btn-over','x-btn-focus'])
            },
            mouseleave: function(){
                this.button.removeClass(['x-btn-over','x-btn-focus','x-btn-click'])
            },
            mousedown: function(){
                this.button.addClass('x-btn-click')
            },
            mouseup: function(){
                this.button.removeClass(['x-btn-over','x-btn-focus','x-btn-click'])
            },
            change: function(){
                var v = this.fileInput.dom.value;
                this.setValue(v);
                this.fireEvent('fileselected', this, v);    
            }
        }); 
    },
    createFileInput : function() {
        this.fileInput = this.wrap.createChild({
            id: this.getFileInputId(),
            name: this.name||this.getId(),
            cls: 'x-form-file',
            tag: 'input',
            type: 'file',
            size: 1
        });
    },
    reset : function(){
        if (this.rendered) {
            this.fileInput.remove();
            this.createFileInput();
            this.bindListeners();
        }
        Ext.ux.form.FileUploadField.superclass.reset.call(this);
    },
    // private
    getFileInputId: function(){
        return this.id + '-file';
    },
    // private
    onResize : function(w, h){
        Ext.ux.form.FileUploadField.superclass.onResize.call(this, w, h);

        this.wrap.setWidth(w);

        if(!this.buttonOnly){
            var w = this.wrap.getWidth() - this.button.getEl().getWidth() - this.buttonOffset;
            this.el.setWidth(w);
        }
    },
    // private
    onDestroy: function(){
        Ext.ux.form.FileUploadField.superclass.onDestroy.call(this);
        Ext.destroy(this.fileInput, this.button, this.wrap);
    },
    onDisable: function(){
        Ext.ux.form.FileUploadField.superclass.onDisable.call(this);
        this.doDisable(true);
    },
    onEnable: function(){
        Ext.ux.form.FileUploadField.superclass.onEnable.call(this);
        this.doDisable(false);

    },
    // private
    doDisable: function(disabled){
        this.fileInput.dom.disabled = disabled;
        this.button.setDisabled(disabled);
    },
    // private
    preFocus : Ext.emptyFn,
    // private
    alignErrorIcon : function(){
        this.errorIcon.alignTo(this.wrap, 'tl-tr', [2, 0]);
    }
});

Ext.reg('fileuploadfield', Ext.ux.form.FileUploadField);

// backwards compat
Ext.form.FileUploadField = Ext.ux.form.FileUploadField;
Ext.ns('Ext.ux.form');
Ext.ux.form.MultiSelect = Ext.extend(Ext.form.Field,  {
   
    ddReorder:false,
    appendOnly:false,

    width:100,

    height:100,

    displayField:0,

    valueField:1,

    allowBlank:true,

    minSelections:0,

    maxSelections:Number.MAX_VALUE,

    blankText:Ext.form.TextField.prototype.blankText,

    minSelectionsText:'Minimum {0} item(s) required',

    maxSelectionsText:'Maximum {0} item(s) allowed',

    delimiter:',',

    cls: 'ux-form-multiselect',

    // private
    defaultAutoCreate : {tag: "div"},

    // private
    initComponent: function(){
        Ext.ux.form.MultiSelect.superclass.initComponent.call(this);

        if(Ext.isArray(this.store)){
            if (Ext.isArray(this.store[0])){
                this.store = new Ext.data.ArrayStore({
                    fields: ['value','text'],
                    data: this.store
                });
                this.valueField = 'value';
            }else{
                this.store = new Ext.data.ArrayStore({
                    fields: ['text'],
                    data: this.store,
                    expandData: true
                });
                this.valueField = 'text';
            }
            this.displayField = 'text';
        } else {
            this.store = Ext.StoreMgr.lookup(this.store);
        }

        this.addEvents({
            'dblclick' : true,
            'click' : true,
            'change' : true,
            'drop' : true
        });
    },

    // private
    onRender: function(ct, position){
        Ext.ux.form.MultiSelect.superclass.onRender.call(this, ct, position);

        var fs = this.fs = new Ext.form.FieldSet({
            renderTo: this.el,
            title: this.legend,
            height: this.height,
            width: this.width,
            style: "padding:0;",
            tbar: this.tbar
        });
        fs.body.addClass('ux-mselect');

        this.view = new Ext.ListView({
            selectedClass: 'ux-mselect-selected',
            multiSelect: true,
            store: this.store,
            columns: [{ header: 'Value', width: 1, dataIndex: this.displayField }],
            hideHeaders: true
        });

        fs.add(this.view);

        this.view.on('click', this.onViewClick, this);
        this.view.on('beforeclick', this.onViewBeforeClick, this);
        this.view.on('dblclick', this.onViewDblClick, this);

        this.hiddenName = this.name || Ext.id();
        var hiddenTag = { tag: "input", type: "hidden", value: "", name: this.hiddenName };
        this.hiddenField = this.el.createChild(hiddenTag);
        this.hiddenField.dom.disabled = this.hiddenName != this.name;
        fs.doLayout();
    },

    // private
    afterRender: function(){
        Ext.ux.form.MultiSelect.superclass.afterRender.call(this);

        if (this.ddReorder && !this.dragGroup && !this.dropGroup){
            this.dragGroup = this.dropGroup = 'MultiselectDD-' + Ext.id();
        }

        if (this.draggable || this.dragGroup){
            this.dragZone = new Ext.ux.form.MultiSelect.DragZone(this, {
                ddGroup: this.dragGroup
            });
        }
        if (this.droppable || this.dropGroup){
            this.dropZone = new Ext.ux.form.MultiSelect.DropZone(this, {
                ddGroup: this.dropGroup
            });
        }
    },

    // private
    onViewClick: function(vw, index, node, e) {
        this.fireEvent('change', this, this.getValue(), this.hiddenField.dom.value);
        this.hiddenField.dom.value = this.getValue();
        this.fireEvent('click', this, e);
        this.validate();
    },

    // private
    onViewBeforeClick: function(vw, index, node, e) {
        if (this.disabled || this.readOnly) {
            return false;
        }
    },

    // private
    onViewDblClick : function(vw, index, node, e) {
        return this.fireEvent('dblclick', vw, index, node, e);
    },

    /**
     * Returns an array of data values for the selected items in the list. The values will be separated
     * by {@link #delimiter}.
     * @return {Array} value An array of string data values
     */
    getValue: function(valueField){
        var returnArray = [];
        var selectionsArray = this.view.getSelectedIndexes();
        if (selectionsArray.length == 0) {return '';}
        for (var i=0; i<selectionsArray.length; i++) {
            returnArray.push(this.store.getAt(selectionsArray[i]).get((valueField != null) ? valueField : this.valueField));
        }
        return returnArray.join(this.delimiter);
    },

    /**
     * Sets a delimited string (using {@link #delimiter}) or array of data values into the list.
     * @param {String/Array} values The values to set
     */
    setValue: function(values) {
        var index;
        var selections = [];
        this.view.clearSelections();
        this.hiddenField.dom.value = '';

        if (!values || (values == '')) { return; }

        if (!Ext.isArray(values)) { values = values.split(this.delimiter); }
        for (var i=0; i<values.length; i++) {
            index = this.view.store.indexOf(this.view.store.query(this.valueField,
                new RegExp('^' + values[i] + '$', "i")).itemAt(0));
            selections.push(index);
        }
        this.view.select(selections);
        this.hiddenField.dom.value = this.getValue();
        this.validate();
    },

    // inherit docs
    reset : function() {
        this.setValue('');
    },

    // inherit docs
    getRawValue: function(valueField) {
        var tmp = this.getValue(valueField);
        if (tmp.length) {
            tmp = tmp.split(this.delimiter);
        }
        else {
            tmp = [];
        }
        return tmp;
    },

    // inherit docs
    setRawValue: function(values){
        setValue(values);
    },

    // inherit docs
    validateValue : function(value){
        if (value.length < 1) { // if it has no value
             if (this.allowBlank) {
                 this.clearInvalid();
                 return true;
             } else {
                 this.markInvalid(this.blankText);
                 return false;
             }
        }
        if (value.length < this.minSelections) {
            this.markInvalid(String.format(this.minSelectionsText, this.minSelections));
            return false;
        }
        if (value.length > this.maxSelections) {
            this.markInvalid(String.format(this.maxSelectionsText, this.maxSelections));
            return false;
        }
        return true;
    },

    // inherit docs
    disable: function(){
        this.disabled = true;
        this.hiddenField.dom.disabled = true;
        this.fs.disable();
    },

    // inherit docs
    enable: function(){
        this.disabled = false;
        this.hiddenField.dom.disabled = false;
        this.fs.enable();
    },

    // inherit docs
    destroy: function(){
        Ext.destroy(this.fs, this.dragZone, this.dropZone);
        Ext.ux.form.MultiSelect.superclass.destroy.call(this);
    }
});


Ext.reg('multiselect', Ext.ux.form.MultiSelect);

//backwards compat
Ext.ux.Multiselect = Ext.ux.form.MultiSelect;


Ext.ux.form.MultiSelect.DragZone = function(ms, config){
    this.ms = ms;
    this.view = ms.view;
    var ddGroup = config.ddGroup || 'MultiselectDD';
    var dd;
    if (Ext.isArray(ddGroup)){
        dd = ddGroup.shift();
    } else {
        dd = ddGroup;
        ddGroup = null;
    }
    Ext.ux.form.MultiSelect.DragZone.superclass.constructor.call(this, this.ms.fs.body, { containerScroll: true, ddGroup: dd });
    this.setDraggable(ddGroup);
};

Ext.extend(Ext.ux.form.MultiSelect.DragZone, Ext.dd.DragZone, {
    onInitDrag : function(x, y){
        var el = Ext.get(this.dragData.ddel.cloneNode(true));
        this.proxy.update(el.dom);
        el.setWidth(el.child('em').getWidth());
        this.onStartDrag(x, y);
        return true;
    },

    // private
    collectSelection: function(data) {
        data.repairXY = Ext.fly(this.view.getSelectedNodes()[0]).getXY();
        var i = 0;
        this.view.store.each(function(rec){
            if (this.view.isSelected(i)) {
                var n = this.view.getNode(i);
                var dragNode = n.cloneNode(true);
                dragNode.id = Ext.id();
                data.ddel.appendChild(dragNode);
                data.records.push(this.view.store.getAt(i));
                data.viewNodes.push(n);
            }
            i++;
        }, this);
    },

    // override
    onEndDrag: function(data, e) {
        var d = Ext.get(this.dragData.ddel);
        if (d && d.hasClass("multi-proxy")) {
            d.remove();
        }
    },

    // override
    getDragData: function(e){
        var target = this.view.findItemFromChild(e.getTarget());
        if(target) {
            if (!this.view.isSelected(target) && !e.ctrlKey && !e.shiftKey) {
                this.view.select(target);
                this.ms.setValue(this.ms.getValue());
            }
            if (this.view.getSelectionCount() == 0 || e.ctrlKey || e.shiftKey) return false;
            var dragData = {
                sourceView: this.view,
                viewNodes: [],
                records: []
            };
            if (this.view.getSelectionCount() == 1) {
                var i = this.view.getSelectedIndexes()[0];
                var n = this.view.getNode(i);
                dragData.viewNodes.push(dragData.ddel = n);
                dragData.records.push(this.view.store.getAt(i));
                dragData.repairXY = Ext.fly(n).getXY();
            } else {
                dragData.ddel = document.createElement('div');
                dragData.ddel.className = 'multi-proxy';
                this.collectSelection(dragData);
            }
            return dragData;
        }
        return false;
    },

    // override the default repairXY.
    getRepairXY : function(e){
        return this.dragData.repairXY;
    },

    // private
    setDraggable: function(ddGroup){
        if (!ddGroup) return;
        if (Ext.isArray(ddGroup)) {
            Ext.each(ddGroup, this.setDraggable, this);
            return;
        }
        this.addToGroup(ddGroup);
    }
});

Ext.ux.form.MultiSelect.DropZone = function(ms, config){
    this.ms = ms;
    this.view = ms.view;
    var ddGroup = config.ddGroup || 'MultiselectDD';
    var dd;
    if (Ext.isArray(ddGroup)){
        dd = ddGroup.shift();
    } else {
        dd = ddGroup;
        ddGroup = null;
    }
    Ext.ux.form.MultiSelect.DropZone.superclass.constructor.call(this, this.ms.fs.body, { containerScroll: true, ddGroup: dd });
    this.setDroppable(ddGroup);
};

Ext.extend(Ext.ux.form.MultiSelect.DropZone, Ext.dd.DropZone, {
    /**
     * Part of the Ext.dd.DropZone interface. If no target node is found, the
     * whole Element becomes the target, and this causes the drop gesture to append.
     */
    getTargetFromEvent : function(e) {
        var target = e.getTarget();
        return target;
    },

    // private
    getDropPoint : function(e, n, dd){
        if (n == this.ms.fs.body.dom) { return "below"; }
        var t = Ext.lib.Dom.getY(n), b = t + n.offsetHeight;
        var c = t + (b - t) / 2;
        var y = Ext.lib.Event.getPageY(e);
        if(y <= c) {
            return "above";
        }else{
            return "below";
        }
    },

    // private
    isValidDropPoint: function(pt, n, data) {
        if (!data.viewNodes || (data.viewNodes.length != 1)) {
            return true;
        }
        var d = data.viewNodes[0];
        if (d == n) {
            return false;
        }
        if ((pt == "below") && (n.nextSibling == d)) {
            return false;
        }
        if ((pt == "above") && (n.previousSibling == d)) {
            return false;
        }
        return true;
    },

    // override
    onNodeEnter : function(n, dd, e, data){
        return false;
    },

    // override
    onNodeOver : function(n, dd, e, data){
        var dragElClass = this.dropNotAllowed;
        var pt = this.getDropPoint(e, n, dd);
        if (this.isValidDropPoint(pt, n, data)) {
            if (this.ms.appendOnly) {
                return "x-tree-drop-ok-below";
            }

            // set the insert point style on the target node
            if (pt) {
                var targetElClass;
                if (pt == "above"){
                    dragElClass = n.previousSibling ? "x-tree-drop-ok-between" : "x-tree-drop-ok-above";
                    targetElClass = "x-view-drag-insert-above";
                } else {
                    dragElClass = n.nextSibling ? "x-tree-drop-ok-between" : "x-tree-drop-ok-below";
                    targetElClass = "x-view-drag-insert-below";
                }
                if (this.lastInsertClass != targetElClass){
                    Ext.fly(n).replaceClass(this.lastInsertClass, targetElClass);
                    this.lastInsertClass = targetElClass;
                }
            }
        }
        return dragElClass;
    },

    // private
    onNodeOut : function(n, dd, e, data){
        this.removeDropIndicators(n);
    },

    // private
    onNodeDrop : function(n, dd, e, data){
        if (this.ms.fireEvent("drop", this, n, dd, e, data) === false) {
            return false;
        }
        var pt = this.getDropPoint(e, n, dd);
        if (n != this.ms.fs.body.dom)
            n = this.view.findItemFromChild(n);

        if(this.ms.appendOnly) {
            insertAt = this.view.store.getCount();
        } else {
            insertAt = n == this.ms.fs.body.dom ? this.view.store.getCount() - 1 : this.view.indexOf(n);
            if (pt == "below") {
                insertAt++;
            }
        }

        var dir = false;

        // Validate if dragging within the same MultiSelect
        if (data.sourceView == this.view) {
            // If the first element to be inserted below is the target node, remove it
            if (pt == "below") {
                if (data.viewNodes[0] == n) {
                    data.viewNodes.shift();
                }
            } else {  // If the last element to be inserted above is the target node, remove it
                if (data.viewNodes[data.viewNodes.length - 1] == n) {
                    data.viewNodes.pop();
                }
            }

            // Nothing to drop...
            if (!data.viewNodes.length) {
                return false;
            }

            // If we are moving DOWN, then because a store.remove() takes place first,
            // the insertAt must be decremented.
            if (insertAt > this.view.store.indexOf(data.records[0])) {
                dir = 'down';
                insertAt--;
            }
        }

        for (var i = 0; i < data.records.length; i++) {
            var r = data.records[i];
            if (data.sourceView) {
                data.sourceView.store.remove(r);
            }
            this.view.store.insert(dir == 'down' ? insertAt : insertAt++, r);
            var si = this.view.store.sortInfo;
            if(si){
                this.view.store.sort(si.field, si.direction);
            }
        }
        return true;
    },

    // private
    removeDropIndicators : function(n){
        if(n){
            Ext.fly(n).removeClass([
                "x-view-drag-insert-above",
                "x-view-drag-insert-left",
                "x-view-drag-insert-right",
                "x-view-drag-insert-below"]);
            this.lastInsertClass = "_noclass";
        }
    },

    // private
    setDroppable: function(ddGroup){
        if (!ddGroup) return;
        if (Ext.isArray(ddGroup)) {
            Ext.each(ddGroup, this.setDroppable, this);
            return;
        }
        this.addToGroup(ddGroup);
    }
});

/*!
 * accounting.js v0.3.2
 * Copyright 2011, Joss Crowcroft
 *
 * Freely distributable under the MIT license.
 * Portions of accounting.js are inspired or borrowed from underscore.js
 *
 * Full details and documentation:
 * http://josscrowcroft.github.com/accounting.js/
 */

(function(root, undefined) {

    /* --- Setup --- */

    // Create the local library object, to be exported or referenced globally later
    var lib = {};

    // Current version
    lib.version = '0.3.2';


    /* --- Exposed settings --- */

    // The library's settings configuration object. Contains default parameters for
    // currency and number formatting
    lib.settings = {
        currency: {
            symbol : "$",        // default currency symbol is '$'
            format : "%s%v",    // controls output: %s = symbol, %v = value (can be object, see docs)
            decimal : ".",        // decimal point separator
            thousand : ",",        // thousands separator
            precision : 2,        // decimal places
            grouping : 3        // digit grouping (not implemented yet)
        },
        number: {
            precision : 0,        // default precision on numbers is 0
            grouping : 3,        // digit grouping (not implemented yet)
            thousand : ",",
            decimal : "."
        }
    };


    /* --- Internal Helper Methods --- */

    // Store reference to possibly-available ECMAScript 5 methods for later
    var nativeMap = Array.prototype.map,
        nativeIsArray = Array.isArray,
        toString = Object.prototype.toString;

    /**
     * Tests whether supplied parameter is a string
     * from underscore.js
     */
    function isString(obj) {
        return !!(obj === '' || (obj && obj.charCodeAt && obj.substr));
    }

    /**
     * Tests whether supplied parameter is a string
     * from underscore.js, delegates to ECMA5's native Array.isArray
     */
    function isArray(obj) {
        return nativeIsArray ? nativeIsArray(obj) : toString.call(obj) === '[object Array]';
    }

    /**
     * Tests whether supplied parameter is a true object
     */
    function isObject(obj) {
        return obj && toString.call(obj) === '[object Object]';
    }

    /**
     * Extends an object with a defaults object, similar to underscore's _.defaults
     *
     * Used for abstracting parameter handling from API methods
     */
    function defaults(object, defs) {
        var key;
        object = object || {};
        defs = defs || {};
        // Iterate over object non-prototype properties:
        for (key in defs) {
            if (defs.hasOwnProperty(key)) {
                // Replace values with defaults only if undefined (allow empty/zero values):
                if (object[key] == null) object[key] = defs[key];
            }
        }
        return object;
    }

    /**
     * Implementation of `Array.map()` for iteration loops
     *
     * Returns a new Array as a result of calling `iterator` on each array value.
     * Defers to native Array.map if available
     */
    function map(obj, iterator, context) {
        var results = [], i, j;

        if (!obj) return results;

        // Use native .map method if it exists:
        if (nativeMap && obj.map === nativeMap) return obj.map(iterator, context);

        // Fallback for native .map:
        for (i = 0, j = obj.length; i < j; i++ ) {
            results[i] = iterator.call(context, obj[i], i, obj);
        }
        return results;
    }

    /**
     * Check and normalise the value of precision (must be positive integer)
     */
    function checkPrecision(val, base) {
        val = Math.round(Math.abs(val));
        return isNaN(val)? base : val;
    }


    /**
     * Parses a format string or object and returns format obj for use in rendering
     *
     * `format` is either a string with the default (positive) format, or object
     * containing `pos` (required), `neg` and `zero` values (or a function returning
     * either a string or object)
     *
     * Either string or format.pos must contain "%v" (value) to be valid
     */
    function checkCurrencyFormat(format) {
        var defaults = lib.settings.currency.format;

        // Allow function as format parameter (should return string or object):
        if ( typeof format === "function" ) format = format();

        // Format can be a string, in which case `value` ("%v") must be present:
        if ( isString( format ) && format.match("%v") ) {

            // Create and return positive, negative and zero formats:
            return {
                pos : format,
                neg : format.replace("-", "").replace("%v", "-%v"),
                zero : format
            };

        // If no format, or object is missing valid positive value, use defaults:
        } else if ( !format || !format.pos || !format.pos.match("%v") ) {

            // If defaults is a string, casts it to an object for faster checking next time:
            return ( !isString( defaults ) ) ? defaults : lib.settings.currency.format = {
                pos : defaults,
                neg : defaults.replace("%v", "-%v"),
                zero : defaults
            };

        }
        // Otherwise, assume format was fine:
        return format;
    }


    /* --- API Methods --- */

    /**
     * Takes a string/array of strings, removes all formatting/cruft and returns the raw float value
     * alias: accounting.`parse(string)`
     *
     * Decimal must be included in the regular expression to match floats (defaults to
     * accounting.settings.number.decimal), so if the number uses a non-standard decimal 
     * separator, provide it as the second argument.
     *
     * Also matches bracketed negatives (eg. "$ (1.99)" => -1.99)
     *
     * Doesn't throw any errors (`NaN`s become 0) but this may change in future
     */
    var unformat = lib.unformat = lib.parse = function(value, decimal) {
        // Recursively unformat arrays:
        if (isArray(value)) {
            return map(value, function(val) {
                return unformat(val, decimal);
            });
        }

        // Fails silently (need decent errors):
        value = value || 0;

        // Return the value as-is if it's already a number:
        if (typeof value === "number") return value;

        // Default decimal point comes from settings, but could be set to eg. "," in opts:
        decimal = decimal || lib.settings.number.decimal;

         // Build regex to strip out everything except digits, decimal point and minus sign:
        var regex = new RegExp("[^0-9-" + decimal + "]", ["g"]),
            unformatted = parseFloat(
                ("" + value)
                .replace(/\((.*)\)/, "-$1") // replace bracketed values with negatives
                .replace(regex, '')         // strip out any cruft
                .replace(decimal, '.')      // make sure decimal point is standard
            );

        // This will fail silently which may cause trouble, let's wait and see:
        return !isNaN(unformatted) ? unformatted : 0;
    };


    /**
     * Implementation of toFixed() that treats floats more like decimals
     *
     * Fixes binary rounding issues (eg. (0.615).toFixed(2) === "0.61") that present
     * problems for accounting- and finance-related software.
     */
    var toFixed = lib.toFixed = function(value, precision) {
        precision = checkPrecision(precision, lib.settings.number.precision);
        var power = Math.pow(10, precision);

        // Multiply up by precision, round accurately, then divide and use native toFixed():
        return (Math.round(lib.unformat(value) * power) / power).toFixed(precision);
    };


    /**
     * Format a number, with comma-separated thousands and custom precision/decimal places
     *
     * Localise by overriding the precision and thousand / decimal separators
     * 2nd parameter `precision` can be an object matching `settings.number`
     */
    var formatNumber = lib.formatNumber = function(number, precision, thousand, decimal) {
        // Resursively format arrays:
        if (isArray(number)) {
            return map(number, function(val) {
                return formatNumber(val, precision, thousand, decimal);
            });
        }

        // Clean up number:
        number = unformat(number);

        // Build options object from second param (if object) or all params, extending defaults:
        var opts = defaults(
                (isObject(precision) ? precision : {
                    precision : precision,
                    thousand : thousand,
                    decimal : decimal
                }),
                lib.settings.number
            ),

            // Clean up precision
            usePrecision = checkPrecision(opts.precision),

            // Do some calc:
            negative = number < 0 ? "-" : "",
            base = parseInt(toFixed(Math.abs(number || 0), usePrecision), 10) + "",
            mod = base.length > 3 ? base.length % 3 : 0;

        // Format the number:
        return negative + (mod ? base.substr(0, mod) + opts.thousand : "") + base.substr(mod).replace(/(\d{3})(?=\d)/g, "$1" + opts.thousand) + (usePrecision ? opts.decimal + toFixed(Math.abs(number), usePrecision).split('.')[1] : "");
    };


    /**
     * Format a number into currency
     *
     * Usage: accounting.formatMoney(number, symbol, precision, thousandsSep, decimalSep, format)
     * defaults: (0, "$", 2, ",", ".", "%s%v")
     *
     * Localise by overriding the symbol, precision, thousand / decimal separators and format
     * Second param can be an object matching `settings.currency` which is the easiest way.
     *
     * To do: tidy up the parameters
     */
    var formatMoney = lib.formatMoney = function(number, symbol, precision, thousand, decimal, format) {
        // Resursively format arrays:
        if (isArray(number)) {
            return map(number, function(val){
                return formatMoney(val, symbol, precision, thousand, decimal, format);
            });
        }

        // Clean up number:
        number = unformat(number);

        // Build options object from second param (if object) or all params, extending defaults:
        var opts = defaults(
                (isObject(symbol) ? symbol : {
                    symbol : symbol,
                    precision : precision,
                    thousand : thousand,
                    decimal : decimal,
                    format : format
                }),
                lib.settings.currency
            ),

            // Check format (returns object with pos, neg and zero):
            formats = checkCurrencyFormat(opts.format),

            // Choose which format to use for this value:
            useFormat = number > 0 ? formats.pos : number < 0 ? formats.neg : formats.zero;

        // Return with currency symbol added:
        return useFormat.replace('%s', opts.symbol).replace('%v', formatNumber(Math.abs(number), checkPrecision(opts.precision), opts.thousand, opts.decimal));
    };


    /**
     * Format a list of numbers into an accounting column, padding with whitespace
     * to line up currency symbols, thousand separators and decimals places
     *
     * List should be an array of numbers
     * Second parameter can be an object containing keys that match the params
     *
     * Returns array of accouting-formatted number strings of same length
     *
     * NB: `white-space:pre` CSS rule is required on the list container to prevent
     * browsers from collapsing the whitespace in the output strings.
     */
    lib.formatColumn = function(list, symbol, precision, thousand, decimal, format) {
        if (!list) return [];

        // Build options object from second param (if object) or all params, extending defaults:
        var opts = defaults(
                (isObject(symbol) ? symbol : {
                    symbol : symbol,
                    precision : precision,
                    thousand : thousand,
                    decimal : decimal,
                    format : format
                }),
                lib.settings.currency
            ),

            // Check format (returns object with pos, neg and zero), only need pos for now:
            formats = checkCurrencyFormat(opts.format),

            // Whether to pad at start of string or after currency symbol:
            padAfterSymbol = formats.pos.indexOf("%s") < formats.pos.indexOf("%v") ? true : false,

            // Store value for the length of the longest string in the column:
            maxLength = 0,

            // Format the list according to options, store the length of the longest string:
            formatted = map(list, function(val, i) {
                if (isArray(val)) {
                    // Recursively format columns if list is a multi-dimensional array:
                    return lib.formatColumn(val, opts);
                } else {
                    // Clean up the value
                    val = unformat(val);

                    // Choose which format to use for this value (pos, neg or zero):
                    var useFormat = val > 0 ? formats.pos : val < 0 ? formats.neg : formats.zero,

                        // Format this value, push into formatted list and save the length:
                        fVal = useFormat.replace('%s', opts.symbol).replace('%v', formatNumber(Math.abs(val), checkPrecision(opts.precision), opts.thousand, opts.decimal));

                    if (fVal.length > maxLength) maxLength = fVal.length;
                    return fVal;
                }
            });

        // Pad each number in the list and send back the column of numbers:
        return map(formatted, function(val, i) {
            // Only if this is a string (not a nested array, which would have already been padded):
            if (isString(val) && val.length < maxLength) {
                // Depending on symbol position, pad after symbol or at index 0:
                return padAfterSymbol ? val.replace(opts.symbol, opts.symbol+(new Array(maxLength - val.length + 1).join(" "))) : (new Array(maxLength - val.length + 1).join(" ")) + val;
            }
            return val;
        });
    };


    /* --- Module Definition --- */

    // Export accounting for CommonJS. If being loaded as an AMD module, define it as such.
    // Otherwise, just add `accounting` to the global object
    if (typeof exports !== 'undefined') {
        if (typeof module !== 'undefined' && module.exports) {
            exports = module.exports = lib;
        }
        exports.accounting = lib;
    } else if (typeof define === 'function' && define.amd) {
        // Return the library as an AMD module:
        define([], function() {
            return lib;
        });
    } else {
        // Use accounting.noConflict to restore `accounting` back to its original value.
        // Returns a reference to the library's `accounting` object;
        // e.g. `var numbers = accounting.noConflict();`
        lib.noConflict = (function(oldAccounting) {
            return function() {
                // Reset the value of the root's `accounting` variable:
                root.accounting = oldAccounting;
                // Delete the noConflict method:
                lib.noConflict = undefined;
                // Return reference to the library to re-assign it:
                return lib;
            };
        })(root.accounting);

        // Declare `fx` on the root (global/window) object:
        root['accounting'] = lib;
    }

    // Root will be `window` in browser or `global` on the server:
}(this));

