# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ProjectApply.money'
        db.delete_column('core_projectapply', 'money')

        # Adding field 'ProjectApply.book_money'
        db.add_column('core_projectapply', 'book_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ProjectApply.book_money_dec'
        db.add_column('core_projectapply', 'book_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectApply.reserch_money'
        db.add_column('core_projectapply', 'reserch_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ProjectApply.reserch_money_dec'
        db.add_column('core_projectapply', 'reserch_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectApply.meet_money'
        db.add_column('core_projectapply', 'meet_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ProjectApply.meet_money_dec'
        db.add_column('core_projectapply', 'meet_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectApply.computer_money'
        db.add_column('core_projectapply', 'computer_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ProjectApply.computer_money_dec'
        db.add_column('core_projectapply', 'computer_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectApply.print_money'
        db.add_column('core_projectapply', 'print_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ProjectApply.print_money_dec'
        db.add_column('core_projectapply', 'print_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectApply.manage_money'
        db.add_column('core_projectapply', 'manage_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ProjectApply.manage_money_dec'
        db.add_column('core_projectapply', 'manage_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'ProjectApply.other_money'
        db.add_column('core_projectapply', 'other_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ProjectApply.other_money_dec'
        db.add_column('core_projectapply', 'other_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ProjectApply.money'
        db.add_column('core_projectapply', 'money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ProjectApply.book_money'
        db.delete_column('core_projectapply', 'book_money')

        # Deleting field 'ProjectApply.book_money_dec'
        db.delete_column('core_projectapply', 'book_money_dec')

        # Deleting field 'ProjectApply.reserch_money'
        db.delete_column('core_projectapply', 'reserch_money')

        # Deleting field 'ProjectApply.reserch_money_dec'
        db.delete_column('core_projectapply', 'reserch_money_dec')

        # Deleting field 'ProjectApply.meet_money'
        db.delete_column('core_projectapply', 'meet_money')

        # Deleting field 'ProjectApply.meet_money_dec'
        db.delete_column('core_projectapply', 'meet_money_dec')

        # Deleting field 'ProjectApply.computer_money'
        db.delete_column('core_projectapply', 'computer_money')

        # Deleting field 'ProjectApply.computer_money_dec'
        db.delete_column('core_projectapply', 'computer_money_dec')

        # Deleting field 'ProjectApply.print_money'
        db.delete_column('core_projectapply', 'print_money')

        # Deleting field 'ProjectApply.print_money_dec'
        db.delete_column('core_projectapply', 'print_money_dec')

        # Deleting field 'ProjectApply.manage_money'
        db.delete_column('core_projectapply', 'manage_money')

        # Deleting field 'ProjectApply.manage_money_dec'
        db.delete_column('core_projectapply', 'manage_money_dec')

        # Deleting field 'ProjectApply.other_money'
        db.delete_column('core_projectapply', 'other_money')

        # Deleting field 'ProjectApply.other_money_dec'
        db.delete_column('core_projectapply', 'other_money_dec')


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
            '_budget_str': ('django.db.models.fields.TextField', [], {'default': "''"}),
            '_expect_desc_str': ('django.db.models.fields.TextField', [], {'default': "''"}),
            '_final_achievement_str': ('django.db.models.fields.TextField', [], {'default': "''"}),
            '_participant_str': ('django.db.models.fields.TextField', [], {'default': "''"}),
            '_pre_achievement_str': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'applicant'", 'to': "orm['core.User']"}),
            'applicant_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'backward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'book_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'book_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'comple_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'computer_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'computer_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'expert'", 'to': "orm['core.User']"}),
            'expert_approve_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'expert_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert_success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feasibility_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'forward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manage_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'manage_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'marketing_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'meet_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'meet_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'other_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'print_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'print_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'project_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_title_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'reserch_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reserch_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'reserch_type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'study_type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'teacher_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'teacher_phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'teacher_remark': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'teacher_unit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
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
            'job_admin_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'job_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'last_degree': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'nation_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'regtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'remark': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'research_speciality': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Role']"}),
            'sex': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        }
    }

    complete_apps = ['core']