from django.forms import ModelForm
from django import forms

import DBGUI.models


class DataRequestForm1(ModelForm):
    valid_time_formats = ['%I:%M %p']
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'datepicker',
            'placeholder': 'Select a start date',
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'datepicker',
            'placeholder': 'Select an end date',
        })
    )
    start_time = forms.TimeField(input_formats=valid_time_formats,
                                 widget=forms.TimeInput(attrs={
                                     'class': 'timepicker',
                                     'placeholder': 'Select a start time'
                                 })
    )
    end_time = forms.TimeField(input_formats=valid_time_formats,
                               widget=forms.TimeInput(attrs={
                                   'class': 'timepicker',
                                   'placeholder': 'Select an end time'
                               })
    )

    class Meta:
        model = DBGUI.models.DataRequest
        fields = ['start_date', 'end_date', 'start_time', 'end_time', 'room']