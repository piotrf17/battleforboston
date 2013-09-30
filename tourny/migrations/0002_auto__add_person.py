# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'tourny_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('localflavor.us.models.USStateField')(default='MA', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('emergency_contact_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('emergency_contact_relation', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('emergency_contact_phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('kyu_or_dan', self.gf('django.db.models.fields.CharField')(default='K', max_length=1)),
            ('belt_color', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('years_training', self.gf('django.db.models.fields.FloatField')()),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('kata', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('kumite', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('team_kumite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('team_kumite_team_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('boston_battle', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boston_battle_team_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('boston_battle_partner_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'tourny', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'tourny_person')


    models = {
        u'tourny.person': {
            'Meta': {'object_name': 'Person'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'belt_color': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'boston_battle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boston_battle_partner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'boston_battle_team_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'emergency_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'emergency_contact_phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'emergency_contact_relation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kata': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'kumite': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'kyu_or_dan': ('django.db.models.fields.CharField', [], {'default': "'K'", 'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('localflavor.us.models.USStateField', [], {'default': "'MA'", 'max_length': '2'}),
            'team_kumite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team_kumite_team_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'years_training': ('django.db.models.fields.FloatField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['tourny']