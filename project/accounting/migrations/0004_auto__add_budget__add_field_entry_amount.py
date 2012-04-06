# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Budget'
        db.create_table('accounting_budget', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.EntryCategory'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('accounting', ['Budget'])

        # Adding field 'Entry.amount'
        db.add_column('accounting_entry', 'amount', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting model 'Budget'
        db.delete_table('accounting_budget')

        # Deleting field 'Entry.amount'
        db.delete_column('accounting_entry', 'amount')
    
    
    models = {
        'accounting.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'accounting.budget': {
            'Meta': {'object_name': 'Budget'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.EntryCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'accounting.entry': {
            'Meta': {'object_name': 'Entry'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
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
