# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Address.floor'
        db.alter_column('representatives_address', 'floor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))


    def backwards(self, orm):

        # Changing field 'Address.floor'
        db.alter_column('representatives_address', 'floor', self.gf('django.db.models.fields.SmallIntegerField')(null=True))


    models = {
        'representatives.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Country']"}),
            'floor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'office_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Representative']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'representatives.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'representatives.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Representative']"})
        },
        'representatives.mandate': {
            'Meta': {'object_name': 'Mandate'},
            'active': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'constituency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Representative']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'short_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'representatives.phone': {
            'Meta': {'object_name': 'Phone'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Representative']"})
        },
        'representatives.representative': {
            'Meta': {'object_name': 'Representative'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'representatives.website': {
            'Meta': {'object_name': 'WebSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'representative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Representative']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['representatives']
