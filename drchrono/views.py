# Create your views here.

#imports
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail,send_mass_mail,get_connection, EmailMultiAlternatives
from .models import PatientDataModel
from .forms import BirthdayEmail
from django.conf import settings
import datetime
import pytz
import requests
from pprint import pprint


#for dashboard
def dashboard(request):
    #check if user is authenticated
    if not request.user.is_authenticated():
        return redirect('/')

    #creating header for the api call
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
    #getting the name of the Doctor
    docName = docData['first_name'] +' ' + docData['last_name']

    # call drchrono api/patients
    patients_url = 'https://drchrono.com/api/patients'
    patient_list = []

    while True:
        r = requests.get(patients_url, headers=headers)
        patient_data = r.json()
        patient_list.extend(patient_data['results'])
        if not patient_data['next']:
            break

    #save data using PatientDataModel
    patient_list2 = []
    for patient in patient_list:
        #give a default bday if not available
        dob = '1000-01-01'
        if patient['date_of_birth']:
            dob = patient['date_of_birth']
	    # print patient['first_name'] + ' '
	    patient_list2.append(patient['first_name'])

        #patient data model
        p = PatientDataModel(
            patient_id=patient['id'],
            first_name=patient['first_name'],
            last_name=patient['last_name'],
            doctor_id=patient['doctor'],
            birthday=dob,
            patient_email=patient['email']
        )
        # saving the patient data model to local database
        p.save()

    #get all patients who have an email id and birthdate
    message = settings.EMAIL_BIRTHDAY_DEFAULT_MESSAGE

    # Using US/Pacific timezone
    my_date = datetime.datetime.now(pytz.timezone('US/Pacific'))
    birthdays = PatientDataModel.objects.filter(birthday__day=my_date.day,birthday__month=my_date.month).exclude(birthday__year=1)
    numOfBirthdays = len(birthdays)
    birthday_email_list = map(lambda x:x['patient_email'],birthdays.values())
    # print birthday_email_list

    # get the bday form
    form = BirthdayEmail(request.POST or None, initial={'message': message})
    confirmation = None

    if form.is_valid():
        # print "Yes------------"
        name = "drchrono team"

        #default subject
        subject = "Happy Birthday from Dr. " + docData['last_name']
        # if subject is added manualy
        if "subject" in request.POST:
            temp = request.POST.get('subject')
            if temp is not None and temp!='':
                subject=temp
        # print subject

        #get the list of patient's selected
        recipient_list = []
        if "recipientsEmail" in request.POST:
            recipientsEmail = request.POST.get('recipientsEmail')
            if not recipientsEmail:
                print "list empty"
            else:
                recipient_list = recipientsEmail.split(';')
        message = form.cleaned_data['message']
        from_email = "dr chrono"

        #sending mass emails and bcc all
        confirmation = ""
        if not recipient_list:
            confirmation="Message sending failed: Patients not selected"
        else:
            msg = EmailMultiAlternatives(subject, message, from_email,[],bcc=recipient_list)
            count = msg.send()
            if count >= 1:
                confirmation = "Birthday wishes sent."

    template = 'dashboard.html'
    context = {'name': docName,'form':form, 'birthdayList':birthdays, 'numberOfBirthdays':numOfBirthdays, 'confirmation':confirmation}
    return render(request, template, context)


def logout_view(request):
    print "in logout"
    logout(request)
    return redirect('/')
