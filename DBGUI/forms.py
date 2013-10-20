from django.forms import ModelForm, ModelChoiceField
from django import forms

from DBGUI.models import Room


class DataRequestForm1(forms.Form):
    iquery = Room.objects.values_list('name', flat=True).distinct()
    iquery_choices = [('', 'None')] + [(id, id) for id in iquery]
    room = forms.ChoiceField(iquery_choices, error_messages={'required': 'Please select a room.'},
                             required=True, widget=forms.Select())

    valid_time_formats = ['%I:%M %p']
    startDate = forms.DateField(error_messages={'required': 'Start date required !'}, widget=forms.DateInput(attrs=
    {
        'class': 'datepicker',
        'placeholder': 'Select a start date'
    }))
    startTime = forms.TimeField(error_messages={'required': 'Start time required !'}, input_formats=valid_time_formats,
                                widget=forms.TimeInput(attrs={
                                    'class': 'timepicker',
                                    'placeholder': 'Select a start time'
                                }))
    endDate = forms.DateField(error_messages={'required': 'End date required !'}, widget=forms.DateInput(attrs=
    {
        'class': 'datepicker',
        'placeholder': 'Select an end date'
    }))
    endTime = forms.TimeField(error_messages={'required': 'End time required !'}, input_formats=valid_time_formats,
                              widget=forms.TimeInput(attrs={
                                  'class': 'timepicker',
                                  'placeholder': 'Select an end time'
                              }))


class addRoom(ModelForm):
    class Meta:
        model = Room