# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('representatives_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('representatives', ['Country'])

        # Adding model 'Representative'
        db.create_table('representatives_representative', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, db_index=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cv', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('representatives', ['Representative'])

        # Adding model 'Email'
        db.create_table('representatives_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.Representative'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('representatives', ['Email'])

        # Adding model 'WebSite'
        db.create_table('representatives_website', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.Representative'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('representatives', ['WebSite'])

        # Adding model 'Address'
        db.create_table('representatives_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.Representative'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.Country'])),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('floor', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('office_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('representatives', ['Address'])

        # Adding model 'Phone'
        db.create_table('representatives_phone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.Representative'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.Address'])),
        ))
        db.send_create_signal('representatives', ['Phone'])

        # Adding model 'Mandate'
        db.create_table('representatives_mandate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('constituency', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('begin_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('representative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.Representative'])),
        ))
        db.send_create_signal('representatives', ['Mandate'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('representatives_country')

        # Deleting model 'Representative'
        db.delete_table('representatives_representative')

        # Deleting model 'Email'
        db.delete_table('representatives_email')

        # Deleting model 'WebSite'
        db.delete_table('representatives_website')

        # Deleting model 'Address'
        db.delete_table('representatives_address')

        # Deleting model 'Phone'
        db.delete_table('representatives_phone')

        # Deleting model 'Mandate'
        db.delete_table('representatives_mandate')


    models = {
        'representatives.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.Country']"}),
            'floor': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
