# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RoomDevice'
        db.create_table(u'DBGUI_roomdevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DBGUI.Room'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DBGUI.Device'])),
        ))
        db.send_create_signal(u'DBGUI', ['RoomDevice'])


    def backwards(self, orm):
        # Deleting model 'RoomDevice'
        db.delete_table(u'DBGUI_roomdevice')


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
        },
        u'DBGUI.roomdevice': {
            'Meta': {'object_name': 'RoomDevice'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DBGUI.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DBGUI.Room']"})
        }
    }

    complete_apps = ['DBGUI']