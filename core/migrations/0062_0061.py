# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProjectExChange.new_project_end_date'
        db.add_column('core_projectexchange', 'new_project_end_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProjectExChange.new_project_end_date'
        db.delete_column('core_projectexchange', 'new_project_end_date')


    models = {
        'core.convertpdftask': {
            'Meta': {'object_name': 'ConvertPDFTask'},
            'documentid': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.document': {
            'Meta': {'object_name': 'Document'},
            'converted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'converted_err': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'doc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pdf': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'})
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
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiver_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'sender_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'document': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Document']"}),
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
            'document': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Document']"}),
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'expert_approve_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'expert_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'expert_success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feasibility_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'file_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
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
            'project_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_no': ('django.db.models.fields.CharField', [], {'default': "'2abe92d11d444c3393e3cce59f417be3'", 'max_length': '25'}),
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
        'core.projectendapply': {
            'Meta': {'object_name': 'ProjectEndApply'},
            'achive_fomat': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Document']"}),
            'file_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'final_achieve_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'final_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '600'}),
            'font_num': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'go_where': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_user_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'mingwei_option': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '600'}),
            'plain_end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['core.Project']"}),
            'real_end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'study_type_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"}),
            'unit_and_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        'core.projectendapplyapplicantachieve': {
            'Meta': {'object_name': 'ProjectEndApplyApplicantAchieve'},
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'end_apply': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'applicant_achieves'", 'to': "orm['core.ProjectEndApply']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'unit_and_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        'core.projectendapplyapprove': {
            'Meta': {'object_name': 'ProjectEndApplyApprove'},
            'approve': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'approve_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'approvetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectEndApply']"}),
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
            'new_project_end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
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
        'core.projectrollbackapply': {
            'Meta': {'object_name': 'ProjectRollbackApply'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'applicant_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'applicant_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_apply': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectApply']"}),
            'project_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
        },
        'core.projectrollbackapplyapprove': {
            'Meta': {'object_name': 'ProjectRollbackApplyApprove'},
            'approve': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.User']"}),
            'approve_opinion': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'approvetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'details': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectRollbackApply']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.projecttype': {
            'Meta': {'object_name': 'ProjectType'},
            'allow_apply': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_project_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'waring_day': ('django.db.models.fields.IntegerField', [], {'default': '20'})
        },
        'core.role': {
            'Meta': {'object_name': 'Role'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'no': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'parent_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['core.Unit']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'regtime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.unitlimitprojecttype': {
            'Meta': {'object_name': 'UnitLimitProjectType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.ProjectType']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'+'", 'to': "orm['core.Unit']"})
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