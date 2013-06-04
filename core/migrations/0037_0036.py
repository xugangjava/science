# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.email'
        db.add_column('core_user', 'email',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Project.applicant_opinion'
        db.add_column('core_project', 'applicant_opinion',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.project_title_name'
        db.add_column('core_project', 'project_title_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25),
                      keep_default=False)

        # Adding field 'Project.study_type_name'
        db.add_column('core_project', 'study_type_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25),
                      keep_default=False)

        # Adding field 'Project.reserch_type_name'
        db.add_column('core_project', 'reserch_type_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25),
                      keep_default=False)

        # Adding field 'Project.teacher_name'
        db.add_column('core_project', 'teacher_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25),
                      keep_default=False)

        # Adding field 'Project.teacher_unit'
        db.add_column('core_project', 'teacher_unit',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25),
                      keep_default=False)

        # Adding field 'Project.teacher_phone'
        db.add_column('core_project', 'teacher_phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25),
                      keep_default=False)

        # Adding field 'Project.teacher_remark'
        db.add_column('core_project', 'teacher_remark',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.expert'
        db.add_column('core_project', 'expert',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['core.User']),
                      keep_default=False)

        # Adding field 'Project.expert_success'
        db.add_column('core_project', 'expert_success',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Project.expert_approve_time'
        db.add_column('core_project', 'expert_approve_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'Project.expert_opinion'
        db.add_column('core_project', 'expert_opinion',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.total_money'
        db.add_column('core_project', 'total_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.book_money'
        db.add_column('core_project', 'book_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.book_money_dec'
        db.add_column('core_project', 'book_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.reserch_money'
        db.add_column('core_project', 'reserch_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.reserch_money_dec'
        db.add_column('core_project', 'reserch_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.meet_money'
        db.add_column('core_project', 'meet_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.meet_money_dec'
        db.add_column('core_project', 'meet_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.computer_money'
        db.add_column('core_project', 'computer_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.computer_money_dec'
        db.add_column('core_project', 'computer_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.print_money'
        db.add_column('core_project', 'print_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.print_money_dec'
        db.add_column('core_project', 'print_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.manage_money'
        db.add_column('core_project', 'manage_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.manage_money_dec'
        db.add_column('core_project', 'manage_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.other_money'
        db.add_column('core_project', 'other_money',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.other_money_dec'
        db.add_column('core_project', 'other_money_dec',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Project.comple_time'
        db.add_column('core_project', 'comple_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'Project.comple_desc'
        db.add_column('core_project', 'comple_desc',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=500),
                      keep_default=False)

        # Adding field 'Project.feasibility_desc'
        db.add_column('core_project', 'feasibility_desc',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=500),
                      keep_default=False)

        # Adding field 'Project.marketing_desc'
        db.add_column('core_project', 'marketing_desc',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=500),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.email'
        db.delete_column('core_user', 'email')

        # Deleting field 'Project.applicant_opinion'
        db.delete_column('core_project', 'applicant_opinion')

        # Deleting field 'Project.project_title_name'
        db.delete_column('core_project', 'project_title_name')

        # Deleting field 'Project.study_type_name'
        db.delete_column('core_project', 'study_type_name')

        # Deleting field 'Project.reserch_type_name'
        db.delete_column('core_project', 'reserch_type_name')

        # Deleting field 'Project.teacher_name'
        db.delete_column('core_project', 'teacher_name')

        # Deleting field 'Project.teacher_unit'
        db.delete_column('core_project', 'teacher_unit')

        # Deleting field 'Project.teacher_phone'
        db.delete_column('core_project', 'teacher_phone')

        # Deleting field 'Project.teacher_remark'
        db.delete_column('core_project', 'teacher_remark')

        # Deleting field 'Project.expert'
        db.delete_column('core_project', 'expert_id')

        # Deleting field 'Project.expert_success'
        db.delete_column('core_project', 'expert_success')

        # Deleting field 'Project.expert_approve_time'
        db.delete_column('core_project', 'expert_approve_time')

        # Deleting field 'Project.expert_opinion'
        db.delete_column('core_project', 'expert_opinion')

        # Deleting field 'Project.total_money'
        db.delete_column('core_project', 'total_money')

        # Deleting field 'Project.book_money'
        db.delete_column('core_project', 'book_money')

        # Deleting field 'Project.book_money_dec'
        db.delete_column('core_project', 'book_money_dec')

        # Deleting field 'Project.reserch_money'
        db.delete_column('core_project', 'reserch_money')

        # Deleting field 'Project.reserch_money_dec'
        db.delete_column('core_project', 'reserch_money_dec')

        # Deleting field 'Project.meet_money'
        db.delete_column('core_project', 'meet_money')

        # Deleting field 'Project.meet_money_dec'
        db.delete_column('core_project', 'meet_money_dec')

        # Deleting field 'Project.computer_money'
        db.delete_column('core_project', 'computer_money')

        # Deleting field 'Project.computer_money_dec'
        db.delete_column('core_project', 'computer_money_dec')

        # Deleting field 'Project.print_money'
        db.delete_column('core_project', 'print_money')

        # Deleting field 'Project.print_money_dec'
        db.delete_column('core_project', 'print_money_dec')

        # Deleting field 'Project.manage_money'
        db.delete_column('core_project', 'manage_money')

        # Deleting field 'Project.manage_money_dec'
        db.delete_column('core_project', 'manage_money_dec')

        # Deleting field 'Project.other_money'
        db.delete_column('core_project', 'other_money')

        # Deleting field 'Project.other_money_dec'
        db.delete_column('core_project', 'other_money_dec')

        # Deleting field 'Project.comple_time'
        db.delete_column('core_project', 'comple_time')

        # Deleting field 'Project.comple_desc'
        db.delete_column('core_project', 'comple_desc')

        # Deleting field 'Project.feasibility_desc'
        db.delete_column('core_project', 'feasibility_desc')

        # Deleting field 'Project.marketing_desc'
        db.delete_column('core_project', 'marketing_desc')


    models = {
        'core.document': {
            'Meta': {'object_name': 'Document'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'version_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'})
        },
        'core.finalachievement': {
            'Meta': {'object_name': 'FinalAchievement'},
            'actor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'apply': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'final_achives'", 'null': 'True', 'blank': 'True', 'to': "orm['core.ProjectApply']"}),
            'atype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'font_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'no': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.levelachievement': {
            'Meta': {'object_name': 'LevelAchievement'},
            'apply': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'level_achives'", 'null': 'True', 'blank': 'True', 'to': "orm['core.ProjectApply']"}),
            'apply_user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'atype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'no': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
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
            'applicant_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'book_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'book_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'comple_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'comple_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'computer_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'computer_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'expert_approve_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'expert_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert_success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feasibility_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manage_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'manage_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'marketing_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'meet_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'meet_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'other_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'print_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'print_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'project_title_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'ptype': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'reserch_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reserch_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'reserch_type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'study_type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'teacher_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'teacher_phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'teacher_remark': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'teacher_unit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'total_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.projectactor': {
            'Meta': {'object_name': 'ProjectActor'},
            'apply': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'actors'", 'null': 'True', 'blank': 'True', 'to': "orm['core.ProjectApply']"}),
            'degree': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'})
        },
        'core.projectapply': {
            'Meta': {'object_name': 'ProjectApply'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'applicant_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'backward_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'book_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'book_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'comple_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'comple_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'computer_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'computer_money_dec': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
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
            'project_no': ('django.db.models.fields.CharField', [], {'default': "'70e382bb1ea64cacb594a8d4ec5c6a53'", 'max_length': '25'}),
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
            'total_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'waring_day': ('django.db.models.fields.IntegerField', [], {'default': '20'})
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
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
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