# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CarrierState.lcm'
        db.alter_column(u'pricecompare_carrierstate', 'lcm', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3))
        # Adding field 'State.terrorism_loss'
        db.add_column(u'pricecompare_state', 'terrorism_loss',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=3, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'CarrierState.lcm'
        db.alter_column(u'pricecompare_carrierstate', 'lcm', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))
        # Deleting field 'State.terrorism_loss'
        db.delete_column(u'pricecompare_state', 'terrorism_loss')


    models = {
        u'pricecompare.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'expense_constant': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pricecompare.carrierstate': {
            'Meta': {'object_name': 'CarrierState'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.Carrier']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcm': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'premium': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.State']"})
        },
        u'pricecompare.classcode': {
            'Meta': {'object_name': 'ClassCode'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pricecompare.industrygroup': {
            'Meta': {'object_name': 'IndustryGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pricecompare.losscost': {
            'Meta': {'object_name': 'LossCost'},
            'class_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.ClassCode']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss_cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.State']"})
        },
        u'pricecompare.state': {
            'Meta': {'object_name': 'State'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_credit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_debit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'terrorism_loss': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'})
        },
        u'pricecompare.statemodifier': {
            'Meta': {'object_name': 'StateModifier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifier': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pricecompare.State']"})
        }
    }

    complete_apps = ['pricecompare']