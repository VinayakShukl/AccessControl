# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Building'
        db.create_table(u'DBGUI_building', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, primary_key=True)),
        ))
        db.send_create_signal(u'DBGUI', ['Building'])

        # Adding model 'Floor'
        db.create_table(u'DBGUI_floor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DBGUI.Building'])),
            ('floor', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'DBGUI', ['Floor'])

        # Adding model 'Room'
        db.create_table(u'DBGUI_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DBGUI.Floor'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'DBGUI', ['Room'])

        # Adding model 'Device'
        db.create_table(u'DBGUI_device', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('dType', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'DBGUI', ['Device'])

        # Adding model 'DataRequest'
        db.create_table(u'DBGUI_datarequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DBGUI.Room'])),
            ('request_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 12, 0, 0))),
            ('request_IP', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal(u'DBGUI', ['DataRequest'])


    def backwards(self, orm):
        # Deleting model 'Building'
        db.delete_table(u'DBGUI_building')

        # Deleting model 'Floor'
        db.delete_table(u'DBGUI_floor')

        # Deleting model 'Room'
        db.delete_table(u'DBGUI_room')

        # Deleting model 'Device'
        db.delete_table(u'DBGUI_device')

        # Deleting model 'DataRequest'
        db.delete_table(u'DBGUI_datarequest')


    models = {
        u'DBGUI.building': {
            'Meta': {'object_name': 'Building'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'primary_key': 'True'})
        },
        u'DBGUI.datarequest': {
            'Meta': {'object_name': 'DataRequest'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_IP': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'request_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 12, 0, 0)'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DBGUI.Room']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'DBGUI.device': {
            'Meta': {'object_name': 'Device'},
            'dType': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'})
        },
        u'DBGUI.floor': {
            'Meta': {'object_name': 'Floor'},
            'bID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DBGUI.Building']"}),
            'floor': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'DBGUI.room': {
            'Meta': {'object_name': 'Room'},
            'fID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DBGUI.Floor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['DBGUI']