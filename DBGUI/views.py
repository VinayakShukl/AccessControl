from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django_tables2_reports.config import RequestConfigReport as RequestConfig
from django_tables2_reports.utils import create_report_http_response

from models import *
from forms import DataRequestForm1

from accesscontrol import get_http_resonse


reqtable = []
chartList = []

def process_form(form, request):
    building_name = form.cleaned_data['room']
    startdate = form.cleaned_data['start_date']
    starttime = form.cleaned_data['start_time']
    enddate = form.cleaned_data['end_date']
    endtime = form.cleaned_data['end_time']
    info = {'room': building_name, 'sTime': datetime.combine(startdate, starttime),
            'eTime': datetime.combine(enddate, endtime), 'rTime': datetime.now(), 'rIP': get_client_ip(request)}
    return info


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    global reqtable, chartList
    form = DataRequestForm1()
    if request.method == 'POST':
        form = DataRequestForm1(request.POST, request)
        if form.is_valid():
            infodict = process_form(form, request)
            reqtable, chartList = get_http_resonse(infodict)
            return redirect('/details/')
        else:
            print form.errors
    return render(request, 'RequestForm.html', {'form': form, 'title': "Access Control"})


def details(request):
    global reqtable, chartList
    #RequestConfig(request).configure(reqTable)
    table_to_report = RequestConfig(request, paginate={"per_page": 15}).configure(reqtable)
    if table_to_report:
        return create_report_http_response(table_to_report, request)
    return render_to_response('details.html',
                              {'title': "Details", 'info': reqtable, 'chart': chartList},
                              context_instance=RequestContext(request))
    #return render(request, 'details.html', {'title': "Details", 'info': reqTable})
