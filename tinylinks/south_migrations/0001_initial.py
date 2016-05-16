# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tinylink'
        db.create_table('tinylinks_tinylink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('long_url', self.gf('django.db.models.fields.CharField')(max_length=2500)),
            ('short_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('tinylinks', ['Tinylink'])


    def backwards(self, orm):
        # Deleting model 'Tinylink'
        db.delete_table('tinylinks_tinylink')


    models = {
        'tinylinks.tinylink': {
            'Meta': {'object_name': 'Tinylink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_url': ('django.db.models.fields.CharField', [], {'max_length': '2500'}),
            'short_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['tinylinks']