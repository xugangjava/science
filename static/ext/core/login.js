/**
 * Created with PyCharm.
 * User: Administrator
 * Date: 12-11-22
 * Time: 下午2:05
 * To change this template use File | Settings | File Templates.
 */

Ext.onReady(function() {
    Ext.QuickTips.init();
    var submit_handler = function () {
        var form = formPanel.getForm();
        if (!form.isValid()) return;
        form.submit({
            clientValidation:true,
            url:'/login/',
            success:function (form, action) {
                if ("OK" == action.result.msg) {
                    window.location.href = '/main/'
                } else {
                    alert(action.result.msg);
                }
            },
            failure:function () {
                error('登录异常！');
            }
        });
    };


    var submit = new Ext.Button({
        xtype: 'button',
        formBind: true,
        text: '登录',
        width: 80,
        handler:submit_handler});

    var formPanel = new Ext.form.FormPanel({
        renderTo: 'content',
        id: 'login_form',
        frame: true,
        width: 350,
        bodyPadding: 10,
        bodyBorder: true,
        title: '国家民委项目申报系统',
        defaults: {
            anchor: '100%'
        },

        fieldDefaults: {
            labelAlign: 'left',
            msgTarget: 'none'
        },
        items: [{
            xtype: 'textfield',
            name: 'name',
            fieldLabel: '用户名',
            allowBlank: false,
            listeners:{
                scope:this,
                specialkey: function(f,e){
                    if(e.getKey()==e.ENTER){
                        submit_handler();
                    }
                }
            }
        }, {
            xtype: 'textfield',
            name: 'password',
            fieldLabel: '密码',
            inputType: 'password',
            allowBlank: false,
            listeners:{
                scope:this,
                specialkey: function(f,e){
                    if(e.getKey()==e.ENTER){
                        submit_handler();
                    }
                }
            }
        }, {
            xtype: 'panel',
            anchor: '100%',
            layout: 'column',
            items: [{
                columnWidth: .7,
                layout: 'form',
                items: [{
                    fieldLabel: '验证码',
                    name: 'code',
                    height: 30,
                    xtype: 'textfield',
                    allowBlank: false,
                    listeners: {
                        scope: this,
                        specialkey: function(f, e) {
                            if (e.getKey() == e.ENTER) {
                                submit_handler();
                            }
                        }
                    }
                }]
            }, {
                columnWidth: .2,
                xtype: 'panel',
                width: 60,
                html: '<img src="/login/code/" onclick="newcode(this)"/>'
            }]
        }],
        buttons: [submit]
    });
    formPanel.el.center();
    window.onresize = function() {
        formPanel.el.center();
    }
});