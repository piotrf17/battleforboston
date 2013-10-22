# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TeamEvent'
        db.create_table(u'tourny_teamevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('experience', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('team_size', self.gf('django.db.models.fields.IntegerField')(default=3)),
        ))
        db.send_create_signal(u'tourny', ['TeamEvent'])

        # Adding M2M table for field competitors on 'TeamEvent'
        m2m_table_name = db.shorten_name(u'tourny_teamevent_competitors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teamevent', models.ForeignKey(orm[u'tourny.teamevent'], null=False)),
            ('team', models.ForeignKey(orm[u'tourny.team'], null=False))
        ))
        db.create_unique(m2m_table_name, ['teamevent_id', 'team_id'])

        # Adding model 'IndividualEvent'
        db.create_table(u'tourny_individualevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('experience', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'tourny', ['IndividualEvent'])

        # Adding M2M table for field competitors on 'IndividualEvent'
        m2m_table_name = db.shorten_name(u'tourny_individualevent_competitors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('individualevent', models.ForeignKey(orm[u'tourny.individualevent'], null=False)),
            ('person', models.ForeignKey(orm[u'tourny.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['individualevent_id', 'person_id'])

        # Adding model 'Team'
        db.create_table(u'tourny_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tourny', ['Team'])

        # Adding M2M table for field members on 'Team'
        m2m_table_name = db.shorten_name(u'tourny_team_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm[u'tourny.team'], null=False)),
            ('person', models.ForeignKey(orm[u'tourny.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['team_id', 'person_id'])


        # Changing field 'Person.payment'
        db.alter_column(u'tourny_person', 'payment_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tourny.Payment'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):
        # Deleting model 'TeamEvent'
        db.delete_table(u'tourny_teamevent')

        # Removing M2M table for field competitors on 'TeamEvent'
        db.delete_table(db.shorten_name(u'tourny_teamevent_competitors'))

        # Deleting model 'IndividualEvent'
        db.delete_table(u'tourny_individualevent')

        # Removing M2M table for field competitors on 'IndividualEvent'
        db.delete_table(db.shorten_name(u'tourny_individualevent_competitors'))

        # Deleting model 'Team'
        db.delete_table(u'tourny_team')

        # Removing M2M table for field members on 'Team'
        db.delete_table(db.shorten_name(u'tourny_team_members'))


        # Changing field 'Person.payment'
        db.alter_column(u'tourny_person', 'payment_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tourny.Payment'], null=True))

    models = {
        u'tourny.individualevent': {
            'Meta': {'object_name': 'IndividualEvent'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'competitors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tourny.Person']", 'symmetrical': 'False'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tourny.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
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
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tourny.Payment']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('localflavor.us.models.USStateField', [], {'default': "'MA'", 'max_length': '2'}),
            'team_kumite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team_kumite_team_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'waiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'years_training': ('django.db.models.fields.FloatField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'tourny.team': {
            'Meta': {'object_name': 'Team'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tourny.Person']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tourny.teamevent': {
            'Meta': {'object_name': 'TeamEvent'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'competitors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tourny.Team']", 'symmetrical': 'False'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'team_size': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        }
    }

    complete_apps = ['tourny']