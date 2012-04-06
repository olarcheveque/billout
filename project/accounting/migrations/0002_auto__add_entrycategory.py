# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'EntryCategory'
        db.create_table('accounting_entrycategory', (
            ('type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('accounting', ['EntryCategory'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'EntryCategory'
        db.delete_table('accounting_entrycategory')
    
    
    models = {
        'accounting.entrycategory': {
            'Meta': {'object_name': 'EntryCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }
    
    complete_apps = ['accounting']
