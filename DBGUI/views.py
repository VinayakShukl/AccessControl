from django.shortcuts import render
from forms import DataRequestForm1


def process_form(form):
    building_name = form.cleaned_data['room']
    startDate = form.cleaned_data['startDate']
    startTime = form.cleaned_data['startTime']
    endDate = form.cleaned_data['endDate']
    endTime = form.cleaned_data['endTime']
    print building_name + " -> " + str(startDate) + ":" + str(startTime) + " TO " + str(endDate) + ":" + str(endTime)


def home(request):
    if request.method == 'POST':
        form = DataRequestForm1(request.POST, request)

        if form.is_valid():
            process_form(form)
            #print form.cleaned_data['startDate'], form.cleaned_data['startTime']
            return render(request, 'RequestForm.html', {'form': form, 'title': "Access Control"})
        else:
            print form.errors
            return render(request, 'RequestForm.html', {'form': form, 'title': "Access Control"})

    else:
        form = DataRequestForm1()
        return render(request, 'RequestForm.html', {'form': form, 'title': "Access Control"})