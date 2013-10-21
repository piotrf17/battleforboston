# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.waiver'
        db.add_column(u'tourny_person', 'waiver',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Person.paid'
        db.add_column(u'tourny_person', 'paid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.waiver'
        db.delete_column(u'tourny_person', 'waiver')

        # Deleting field 'Person.paid'
        db.delete_column(u'tourny_person', 'paid')


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
            'college_age': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('localflavor.us.models.USStateField', [], {'default': "'MA'", 'max_length': '2'}),
            'team_kumite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team_kumite_team_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'waiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'years_training': ('django.db.models.fields.FloatField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['tourny']