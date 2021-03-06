# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.regtime'
        db.add_column('core_user', 'regtime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 11, 24, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.regtime'
        db.delete_column('core_user', 'regtime')


    models = {
        'core.approve': {
            'Meta': {'object_name': 'Approve'},
            'approvetime': ('django.db.models.fields.DateTimeField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.MessageType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'receiver_unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Unit']"}),
            'sender_unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.messagetype': {
            'Meta': {'object_name': 'MessageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'proposer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.User']"}),
            'ptype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.ProjectStatus']"})
        },
        'core.projectstatus': {
            'Meta': {'object_name': 'ProjectStatus'},
            'approve': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['core.Approve']"}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'core.projecttype': {
            'Meta': {'object_name': 'ProjectType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'core.role': {
            'Meta': {'object_name': 'Role'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'core.unit': {
            'Meta': {'object_name': 'Unit'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_project': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'parent_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Unit']", 'null': 'True', 'blank': 'True'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'regtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 24, 0, 0)', 'blank': 'True'}),
            'remark': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Role']"}),
            'sex': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Unit']"})
        }
    }

    complete_apps = ['core']