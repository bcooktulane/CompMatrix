# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Carrier.code'
        db.alter_column(u'pricecompare_carrier', 'code', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'Carrier.code'
        db.alter_column(u'pricecompare_carrier', 'code', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'pricecompare.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
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