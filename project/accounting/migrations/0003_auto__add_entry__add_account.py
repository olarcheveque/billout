# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('accounting_entry', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.EntryCategory'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.Account'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('accounting', ['Entry'])

        # Adding model 'Account'
        db.create_table('accounting_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('accounting', ['Account'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('accounting_entry')

        # Deleting model 'Account'
        db.delete_table('accounting_account')
    
    
    models = {
        'accounting.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'accounting.entry': {
            'Meta': {'object_name': 'Entry'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.Account']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.EntryCategory']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'accounting.entrycategory': {
            'Meta': {'object_name': 'EntryCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }
    
    complete_apps = ['accounting']
