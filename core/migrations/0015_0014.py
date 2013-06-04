# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectExChangeApprove'
        db.create_table('core_projectexchangeapprove', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approve', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.User'])),
            ('approvetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('approve_opinion', self.gf('django.db.models.fields.TextField')(default='', max_length=200)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('details', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.ProjectExChange'])),
        ))
        db.send_create_signal('core', ['ProjectExChangeApprove'])

        # Adding model 'ProjectApplyApprove'
        db.create_table('core_projectapplyapprove', (
            ('projectexchangeapprove_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.ProjectExChangeApprove'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('core', ['ProjectApplyApprove'])

        # Deleting field 'ProjectExChange.approve_opinion'
        db.delete_column('core_projectexchange', 'approve_opinion')

        # Deleting field 'ProjectExChange.approvetime'
        db.delete_column('core_projectexchange', 'approvetime')

        # Deleting field 'ProjectExChange.success'
        db.delete_column('core_projectexchange', 'success')

        # Deleting field 'ProjectExChange.approve'
        db.delete_column('core_projectexchange', 'approve')


        # Renaming column for 'ProjectExChange.applicant' to match new field type.
        db.rename_column('core_projectexchange', 'applicant', 'applicant_id')
        # Changing field 'ProjectExChange.applicant'
        db.alter_column('core_projectexchange', 'applicant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User']))
        # Adding index on 'ProjectExChange', fields ['applicant']
        db.create_index('core_projectexchange', ['applicant_id'])


    def backwards(self, orm):
        # Removing index on 'ProjectExChange', fields ['applicant']
        db.delete_index('core_projectexchange', ['applicant_id'])

        # Deleting model 'ProjectExChangeApprove'
        db.delete_table('core_projectexchangeapprove')

        # Deleting model 'ProjectApplyApprove'
        db.delete_table('core_projectapplyapprove')

        # Adding field 'ProjectExChange.approve_opinion'
        db.add_column('core_projectexchange', 'approve_opinion',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectExChange.approvetime'
        db.add_column('core_projectexchange', 'approvetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ProjectExChange.success'
        db.add_column('core_projectexchange', 'success',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProjectExChange.approve'
        db.add_column('core_projectexchange', 'approve',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=25),
                      keep_default=False)


        # Renaming column for 'ProjectExChange.applicant' to match new field type.
        db.rename_column('core_projectexchange', 'applicant_id', 'applicant')
        # Changing field 'ProjectExChange.applicant'
        db.alter_column('core_projectexchange', 'applicant', self.gf('django.db.models.fields.CharField')(max_length=25))

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
            'Meta': {'object_name': 'ProjectApplyApprove', '_ormbases': ['core.ProjectExChangeApprove']},
            'projectexchangeapprove_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.ProjectExChangeApprove']", 'unique': 'True', 'primary_key': 'True'})
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