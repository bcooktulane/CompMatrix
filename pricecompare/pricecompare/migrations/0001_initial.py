# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'State'
        db.create_table(u'pricecompare_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'pricecompare', ['State'])

        # Adding model 'Carrier'
        db.create_table(u'pricecompare_carrier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('group', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'pricecompare', ['Carrier'])

        # Adding model 'IndustryGroup'
        db.create_table(u'pricecompare_industrygroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'pricecompare', ['IndustryGroup'])

        # Adding model 'ClassCode'
        db.create_table(u'pricecompare_classcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('industry_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pricecompare.Carrier'])),
        ))
        db.send_create_signal(u'pricecompare', ['ClassCode'])

        # Adding model 'LostCost'
        db.create_table(u'pricecompare_lostcost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pricecompare.State'])),
            ('class_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pricecompare.ClassCode'])),
            ('lost_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'pricecompare', ['LostCost'])

        # Adding model 'CarrierState'
        db.create_table(u'pricecompare_carrierstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('carrier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pricecompare.Carrier'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pricecompare.State'])),
            ('lcm', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('premium', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'pricecompare', ['CarrierState'])


    def backwards(self, orm):
        # Deleting model 'State'
        db.delete_table(u'pricecompare_state')

        # Deleting model 'Carrier'
        db.delete_table(u'pricecompare_carrier')

        # Deleting model 'IndustryGroup'
        db.delete_table(u'pricecompare_industrygroup')

        # Deleting model 'ClassCode'
        db.delete_table(u'pricecompare_classcode')

        # Deleting model 'LostCost'
        db.delete_table(u'pricecompare_lostcost')

        # Deleting model 'CarrierState'
        db.delete_table(u'pricecompare_carrierstate')


    models = {
        u'pricecompare.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'group': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pricecompare.carrierstate': {
            'Meta': {'object_name': 'CarrierState'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.Carrier']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcm': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'premium': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.State']"})
        },
        u'pricecompare.classcode': {
            'Meta': {'object_name': 'ClassCode'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.Carrier']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pricecompare.industrygroup': {
            'Meta': {'object_name': 'IndustryGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pricecompare.lostcost': {
            'Meta': {'object_name': 'LostCost'},
            'class_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.ClassCode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lost_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.State']"})
        },
        u'pricecompare.state': {
            'Meta': {'object_name': 'State'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['pricecompare']