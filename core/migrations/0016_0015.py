# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ProjectApplyApprove.projectexchangeapprove_ptr'
        db.delete_column('core_projectapplyapprove', 'projectexchangeapprove_ptr_id')

        # Adding field 'ProjectApplyApprove.id'
        db.add_column('core_projectapplyapprove', 'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Adding field 'ProjectApplyApprove.approve'
        db.add_column('core_projectapplyapprove', 'approve',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.User']),
                      keep_default=False)

        # Adding field 'ProjectApplyApprove.approvetime'
        db.add_column('core_projectapplyapprove', 'approvetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ProjectApplyApprove.approve_opinion'
        db.add_column('core_projectapplyapprove', 'approve_opinion',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectApplyApprove.success'
        db.add_column('core_projectapplyapprove', 'success',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProjectApplyApprove.details'
        db.add_column('core_projectapplyapprove', 'details',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.ProjectApply']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ProjectApplyApprove.projectexchangeapprove_ptr'
        db.add_column('core_projectapplyapprove', 'projectexchangeapprove_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['core.ProjectExChangeApprove'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProjectApplyApprove.id'
        db.delete_column('core_projectapplyapprove', 'id')

        # Deleting field 'ProjectApplyApprove.approve'
        db.delete_column('core_projectapplyapprove', 'approve_id')

        # Deleting field 'ProjectApplyApprove.approvetime'
        db.delete_column('core_projectapplyapprove', 'approvetime')

        # Deleting field 'ProjectApplyApprove.approve_opinion'
        db.delete_column('core_projectapplyapprove', 'approve_opinion')

        # Deleting field 'ProjectApplyApprove.success'
        db.delete_column('core_projectapplyapprove', 'success')

        # Deleting field 'ProjectApplyApprove.details'
        db.delete_column('core_projectapplyapprove', 'details_id')


    models = {
        'core.expertapprove': {
            'Meta': {'object_name': 'ExpertApprove'},
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'expert_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Project']"}),
            'succes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtype': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.MessageType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'receiver_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"}),
            'sender_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.messagetype': {
            'Meta': {'object_name': 'MessageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'expert_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'ptype': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.projectapply': {
            'Meta': {'object_name': 'ProjectApply', '_ormbases': ['core.ProjectExChange']},
            'projectexchange_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.ProjectExChange']", 'unique': 'True', 'primary_key': 'True'})
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
            'applicanttime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'backward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'forward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Project']"})
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