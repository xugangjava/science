# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ProjectApply.expert_time'
        db.delete_column('core_projectapply', 'expert_time')

        # Adding field 'ProjectApply.expert_success'
        db.add_column('core_projectapply', 'expert_success',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProjectApply.expert_approve_time'
        db.add_column('core_projectapply', 'expert_approve_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ProjectApply.expert_time'
        db.add_column('core_projectapply', 'expert_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Deleting field 'ProjectApply.expert_success'
        db.delete_column('core_projectapply', 'expert_success')

        # Deleting field 'ProjectApply.expert_approve_time'
        db.delete_column('core_projectapply', 'expert_approve_time')


    models = {
        'core.document': {
            'Meta': {'object_name': 'Document'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'version_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'})
        },
        'core.message': {
            'Meta': {'object_name': 'Message'},
            'abstract': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'sender_real_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'sender_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'})
        },
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'ptype': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.projectapply': {
            'Meta': {'object_name': 'ProjectApply'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'applicant'", 'to': "orm['core.User']"}),
            'applicant_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'backward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'expert'", 'to': "orm['core.User']"}),
            'expert_approve_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'expert_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert_success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.projectapplyapprove': {
            'Meta': {'object_name': 'ProjectApplyApprove'},
            'approve': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'approve_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'approvetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectApply']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.projectexchange': {
            'Meta': {'object_name': 'ProjectExChange'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'applicant_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'backward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'forward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Project']"}),
            'project_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.projectexchangeapprove': {
            'Meta': {'object_name': 'ProjectExChangeApprove'},
            'approve': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'approve_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'approvetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectExChange']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'apply_endtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'apply_starttime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_project': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'parent_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['core.Unit']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['core.ProjectType']"}),
            'regtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.user': {
            'Meta': {'object_name': 'User'},
            'approve_opinion': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'approve_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'regtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'remark': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Role']"}),
            'sex': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        }
    }

    complete_apps = ['core']