# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionPattern'
        db.create_table(u'codata_questionpattern', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['codata.Module'])),
            ('pattern_str', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'codata', ['QuestionPattern'])

        # Adding field 'Module.pymodule'
        db.add_column(u'codata_module', 'pymodule',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'QuestionPattern'
        db.delete_table(u'codata_questionpattern')

        # Deleting field 'Module.pymodule'
        db.delete_column(u'codata_module', 'pymodule')


    models = {
        u'codata.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'codata.module': {
            'Meta': {'object_name': 'Module'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['codata.DataSource']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'pymodule': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'codata.questionpattern': {
            'Meta': {'object_name': 'QuestionPattern'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['codata.Module']"}),
            'pattern_str': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['codata']