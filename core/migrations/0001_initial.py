# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table('core_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['Role'])

        # Adding model 'ProjectType'
        db.create_table('core_projecttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('core', ['ProjectType'])

        # Adding model 'Unit'
        db.create_table('core_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('parent_unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Unit'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('project_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.ProjectType'])),
            ('max_project', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['Unit'])

        # Adding model 'User'
        db.create_table('core_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sex', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Unit'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Role'])),
            ('remark', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['User'])

        # Adding model 'MessageType'
        db.create_table('core_messagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('core', ['MessageType'])

        # Adding model 'Message'
        db.create_table('core_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('mtype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.MessageType'])),
            ('sender_unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Unit'])),
            ('receiver_unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.Unit'])),
        ))
        db.send_create_signal('core', ['Message'])

        # Adding model 'Approve'
        db.create_table('core_approve', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approvetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('core', ['Approve'])

        # Adding model 'ProjectStatus'
        db.create_table('core_projectstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('approve', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['core.Approve'])),
        ))
        db.send_create_signal('core', ['ProjectStatus'])

        # Adding model 'Project'
        db.create_table('core_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('ptype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.ProjectType'])),
            ('no', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('proposer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.User'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['core.ProjectStatus'])),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Project'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table('core_role')

        # Deleting model 'ProjectType'
        db.delete_table('core_projecttype')

        # Deleting model 'Unit'
        db.delete_table('core_unit')

        # Deleting model 'User'
        db.delete_table('core_user')

        # Deleting model 'MessageType'
        db.delete_table('core_messagetype')

        # Deleting model 'Message'
        db.delete_table('core_message')

        # Deleting model 'Approve'
        db.delete_table('core_approve')

        # Deleting model 'ProjectStatus'
        db.delete_table('core_projectstatus')

        # Deleting model 'Project'
        db.delete_table('core_project')


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
            'remark': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Role']"}),
            'sex': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['core.Unit']"})
        }
    }

    complete_apps = ['core']