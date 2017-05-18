# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import logout as drchrono_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail,send_mass_mail
from .models import PatientDataModel
from .forms import BirthdayEmail
from django.conf import settings
import datetime
import pytz
import requests
from pprint import pprint

# def home(request):
#     if not request.user.is_authenticated():
#         return redirect('/')
#
#     user_instance = request.user.social_auth.get()
#     access_token = user_instance.extra_data['access_token']
#     headers = {
#         'Authorization': 'Bearer %s' % access_token,
#     }
#
#     # call drchrono api/doctors
#     response = requests.get('https://drchrono.com/api/doctors', headers=headers)
#     response.raise_for_status()
#     data = response.json()
#     docData = data['results'][0]
#     docName = docData['first_name'] +' ' + docData['last_name']
#
#     # this endpoint returns a few lists of patients at a time
#     # it has next and previous points to indicate if more patients are available
#     patients_url = 'https://drchrono.com/api/patients'
#     patient_list = []
#
#     while True:
#         r = requests.get(patients_url, headers=headers)
#         patient_data = r.json()
#         patient_list.extend(patient_data['results'])
#         if not patient_data['next']:
#             break
#
#     #save data using PatientModel
#     patient_list2 = []
#     for patient in patient_list:
#         dob = '1000-01-01'
#         if patient['date_of_birth']:
#             dob = patient['date_of_birth']
# 	    print patient['first_name'] + ' '
# 	    patient_list2.append(patient['first_name'])
#
#         p = PatientDataModel(
#             patient_id=patient['id'],
#             first_name=patient['first_name'],
#             last_name=patient['last_name'],
#             doctor_id=patient['doctor'],
#             birthday=dob,
#             patient_email=patient['email']
#         )
#         p.save()
#     t = get_template('home.html')
#     html = t.render(Context({'name': docName,'patientList':patient_list2}))
#
#     return HttpResponse(html)

def dashboard(request):
    if not request.user.is_authenticated():
        return redirect('/')

    user_instance = request.user.social_auth.get()
    access_token = user_instance.extra_data['access_token']
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    # call drchrono api/doctors
    response = requests.get('https://drchrono.com/api/doctors', headers=headers)
    response.raise_for_status()
    data = response.json()
    docData = data['results'][0]
    docName = docData['first_name'] +' ' + docData['last_name']

    # this endpoint returns a few lists of patients at a time
    # it has next and previous points to indicate if more patients are available
    patients_url = 'https://drchrono.com/api/patients'
    patient_list = []

    while True:
        r = requests.get(patients_url, headers=headers)
        patient_data = r.json()
        patient_list.extend(patient_data['results'])
        if not patient_data['next']:
            break

    #save data using PatientModel
    patient_list2 = []
    for patient in patient_list:
        dob = '1000-01-01'
        if patient['date_of_birth']:
            dob = patient['date_of_birth']
	    # print patient['first_name'] + ' '
	    patient_list2.append(patient['first_name'])

        p = PatientDataModel(
            patient_id=patient['id'],
            first_name=patient['first_name'],
            last_name=patient['last_name'],
            doctor_id=patient['doctor'],
            birthday=dob,
            patient_email=patient['email']
        )
        p.save()

    #get all patients who have an email id and birthdate
    message = settings.EMAIL_BIRTHDAY_DEFAULT_MESSAGE
    # p = PatientDataModel.objects.exclude(patient_email="")
    my_date = datetime.datetime.now(pytz.timezone('US/Pacific'))
#    print my_date.day
    birthdays = PatientDataModel.objects.filter(birthday__day=my_date.day,birthday__month=my_date.month).exclude(birthday__year=1)
    numOfBirthdays = len(birthdays)
    birthday_email_list = map(lambda x:x['patient_email'],birthdays.values())
    # print birthday_email_list
    form = BirthdayEmail(request.POST or None, initial={'message': message})
    confirmation = None

    if form.is_valid():
        # print "Yes------------"
        name = "drchrono team"
        subject = "Happy Birthday"
        if "subject" in request.POST:
            subject = request.POST.get('subject')

        recipient_list = birthday_email_list
        if "recipientsEmail" in request.POST:
            recipientsEmail = request.POST.get('recipientsEmail')
            recipient_list = recipientsEmail.split(';')
        # print recipient_list

        message = form.cleaned_data['message']
        from_email = "drchrono@drchrono.com"
        #sending mass emails
        email_tuple = ((subject, message, from_email, recipient_list),)
        count = send_mass_mail(email_tuple, fail_silently=False)
        confirmation = ""
        if count >= 1:
            confirmation = "Birthday wishes sent."

    template = 'dashboard.html'
    context = {'name': docName,'form':form, 'birthdayList':birthdays, 'numberOfBirthdays':numOfBirthdays, 'confirmation':confirmation}
    return render(request, template, context)

# def createEmail(request):
#     #get all patients who have an email id and birthdate
#     message = settings.EMAIL_BIRTHDAY_DEFAULT_MESSAGE
#     p = PatientDataModel.objects.exclude(patient_email="")
#     my_date = datetime.datetime.now(pytz.timezone('US/Pacific'))
# #    print my_date.day
#     birthdays = PatientDataModel.objects.filter(birthday__day=my_date.day,birthday__month=my_date.month).exclude(birthday__year=1)
#     birthday_email_list = map(lambda x:x['patient_email'],birthdays.values())
#     print birthday_email_list
#     form = BirthdayEmail(request.POST or None, initial={'message': message})
#     confirmation = None
#
#     if form.is_valid():
#         print "Yes------------"
#         name = "drchrono team"
#         subject = "Happy Birthday!"
#         message = form.cleaned_data['message']
#         from_email = "drchrono@drchrono.com"
#         recipient_list = birthday_email_list
#         print recipient_list
#         #sending mass emails
#         email_tuple = ((subject, message, from_email, recipient_list),)
#         count = send_mass_mail(email_tuple, fail_silently=False)
#         confirmation = "Birthday wishes were sent to %s people." % count
#
#     template = 'createEmail.html'
#     context = {'patientList': p, 'form': form, 'confirmation': confirmation, 'birthdays': birthdays}
#     return render(request, template, context)
#
# def sendEmail(request):
#     p = PatientDataModel.objects.exclude(patient_email="")
#     t = get_template('sendEmail.html')
#     html = t.render(Context({'patientList': p}))
#     return HttpResponse(html)
