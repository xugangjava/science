# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProjectTran'
        db.delete_table('core_projecttran')

        # Adding model 'ProjectExChange'
        db.create_table('core_projectexchange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('applicant_opinion', self.gf('django.db.models.fields.TextField')(default='', max_length=200)),
            ('applicanttime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('approve', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('approvetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('approve_opinion', self.gf('django.db.models.fields.TextField')(default='', max_length=200)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('forward_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('backward_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.Project'])),
        ))
        db.send_create_signal('core', ['ProjectExChange'])

        # Adding model 'ExpertApprove'
        db.create_table('core_expertapprove', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expert', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.User'])),
            ('expert_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('expert_opinion', self.gf('django.db.models.fields.TextField')(default='', max_length=200)),
            ('succes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.Project'])),
        ))
        db.send_create_signal('core', ['ExpertApprove'])

        # Adding model 'ProjectApply'
        db.create_table('core_projectapply', (
            ('projectexchange_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.ProjectExChange'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('core', ['ProjectApply'])


    def backwards(self, orm):
        # Adding model 'ProjectTran'
        db.create_table('core_projecttran', (
            ('applicanttime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')(default='', max_length=200)),
            ('approve_opinion', self.gf('django.db.models.fields.TextField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approvetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('applicant', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.Project'])),
            ('forward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('backward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('approve', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('core', ['ProjectTran'])

        # Deleting model 'ProjectExChange'
        db.delete_table('core_projectexchange')

        # Deleting model 'ExpertApprove'
        db.delete_table('core_expertapprove')

        # Deleting model 'ProjectApply'
        db.delete_table('core_projectapply')


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
        'core.projectexchange': {
            'Meta': {'object_name': 'ProjectExChange'},
            'applicant': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'applicant_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'applicanttime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'approve': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'approve_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'approvetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'backward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'forward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Project']"}),
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