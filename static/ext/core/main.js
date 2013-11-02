
Ext.ns('Main');
Ext.onReady(function() {
    //tab
    Main.tab_panel = new Ext.TabPanel({
        id:'MainView',
        resizeTabs:true,
        enableTabScroll:true,
        region:'center'
    });

    Main.welcome_tab=Main.tab_panel.add({
        closable: false,
        id: '欢迎登陆',
        title:'欢迎登陆',
        layout: {
            type: 'fit'
        },
        items: [{
            xtype:'panel',
            frame:true,
            layout:'vbox',
            items:[
                {
                    xtype:'basegrid',
                    url:"/message/list/",
                    autoHeight:true,
                    nocheck:true,
                    notbar:true,
                    nopadding:true,
                    columes:[
                        {
                            header:'消息标题', 
                            dataIndex:'title', 
                            flex:1, 
                            renderer:function(value){
                                return '<img src="/static/icons/zoom.png"/>'+value;
                            }.createDelegate(this)
                        },
                        {header:'消息摘要', dataIndex:'abstract', flex:1 },
                        {header:'发送时间', dataIndex:'send_time', flex:1 },
                        {header:'发送人', dataIndex:'sender_name', flex:1 },
                        {header:'发送姓名', dataIndex:'sender_real_name', flex:1 },
                        {header:'发送部门', dataIndex:'sender_unit__name', flex:1 }
                    ],
                    listeners:{
                        cellclick:DefaultCellHanlder({
                            messageIdx:0
                        })
                    }
                }
            ]
        }]
    });
    Main.tab_panel.setActiveTab(Main.welcome_tab);
    Main.ClearTab=function(){
        Main.tab_panel.items.each(function(item){
            if(item.closable){
               Main.tab_panel.remove(item.id);
            }
        });
    };
    Main.CurrentGrid=function(){
        return Main.tab_panel.getActiveTab().items.items[0];
    };
    // create the Tree
    Main.tree = new Ext.tree.TreePanel({
        hideHeaders: true,
        rootVisible: false,
        width: 180,
        region: "west",
        useArrows: true,
        frame:true,
        collapsible: true,
        store: Main.treeLoader,
        fields: ['list','text','view'],
        root: {
            text: 'hidden',
            id: 'src',
            expanded: true,
            children: []
        },
        listeners: {
            click: function(node, e) {
                Main.ClearTab();
                if(node.attributes.list||node.attributes.view) {
                    var exisTab = Main.tab_panel.findById(node.attributes.text);
                    if(!exisTab) {
                        var grid
                        if(node.attributes.list){
                            grid=new XG.Control.AbstractGrid(node.attributes.list);
                        }
                        else if(node.attributes.view){
                            grid=node.attributes.view;
                        }
                        exisTab = Main.tab_panel.add({
                            closable: true,
                            closeAction:'close',
                            id: node.attributes.text,
                            title: node.attributes.text,
                            layout: {
                                type: 'fit'
                            },
                            items: [grid]
                        });
                        exisTab.show();
                    }
                    Main.tab_panel.setActiveTab(exisTab);
                }
            }
        }
    });
    Main.viewport =new Ext.Viewport({
        layout: {
            type: 'border',
            padding: 5
        },

        defaults: {
            split: true
        },
        items: [{
            id: "head_panel",
            region: "north",
            xtype:'panel',
            height: 120,
           //frame:true,
            layout:'fit',
            split:false,
            border:false,
            items:[
                {
                    xtype:'panel',
                    border:false,
                    html:'<div id="index_head" class="index_head"></div>'
                }
            ]
        },
        Main.tab_panel, 
        Main.tree,
        {
            region: "south",
            xtype:'panel',
            height: 35,
            split:false,
            border:false,           
            //frame:true,
            html:'<div id="index_main_r_foot" class="index_main_r_foot"></div>'
        }]
    });

    Main.MessageWindow=false;
    Main.NotifyMeAgain=true;
    Main.PrevMessage=null;
    var query_message=function(){
        var show_message=function(message){
            Main.PrevMessage=message;
            if(!message)return;
            if(!Main.NotifyMeAgain&&Main.PrevMessage==message)return;
            if(Main.MessageWindow)return;
            Main.MessageWindow=new Ext.ux.Notification({
                iconCls:    'Applicationxpterminal',
                title:      '系统提示',
                html:       message,
                autoDestroy: false,
                hideDelay:  4000,
                width:300,
                height:200,
                listeners:{
                    'destroy':function(cmp){
                        Main.MessageWindow=false;
                    }    
                }
            });
            Main.MessageWindow.addButton({
                text:'我知道了，不再提示！',
                handler:function(){
                    Main.NotifyMeAgain=false;
                    Main.MessageWindow.close();
                }   
            });
            Main.MessageWindow.show('MainView');
       
        }
        Ext.Ajax.request({  
            url:'/message/notify/',
            method:'post',  
            success:function(response,options){
                var res = Ext.util.JSON.decode(response.responseText);
                var onlinecount=res.onlinecount;
                var logincount=res.logincount;
                var lastip=res.lastip;

                if(res.warings){
                    Main.WaringProjects=res.warings.split(',');
                }else{
                    Main.WaringProjects=[];
                }

                var info ="&nbsp;&nbsp;当前系统在线人数:"+onlinecount+"人,";
                info+="您的登录次数:"+logincount+",";
                info+="最后登录IP地址为:"+lastip+",";
                info+="申报问题请咨询您单位管理员<"+Main.AdminRealName+">,"
                info+="联系电话:"+Main.AdminPhone;
    
                Ext.get("index_main_r_foot").dom.innerHTML =info;
                if(res.msg!='OK'){
                    show_message(res.msg);
                }
            }
        });

    }

    Ext.TaskMgr.start({
        run: query_message,
        interval: 30000
    });


});