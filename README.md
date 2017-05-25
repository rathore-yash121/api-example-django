# drchrono Hackathon

### Requirements
- [pip](https://pip.pypa.io/en/stable/)
- [python virtual env](https://packaging.python.org/installing/#creating-and-using-virtual-environments)

### Setup
``` bash
$ pip install -r requirements.txt
$ python manage.py runserver
```

`social_auth_drchrono/` contains a custom provider for [Python Social Auth](http://psa.matiasaguirre.net/) that handles OAUTH for drchrono. To configure it, set these fields in your `drchrono/settings.py` file:

```
SOCIAL_AUTH_DRCHRONO_KEY
SOCIAL_AUTH_DRCHRONO_SECRET
SOCIAL_AUTH_DRCHRONO_SCOPE
LOGIN_REDIRECT_URL

EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```

### Features
  - Created a django application for the doctors to wish their patients on their birthdays.
  - Provided a cool UI which syncs a little with drchrono UI.
  - Login page provides the option of user authorization through Drchrono login credentials.
  - Dashboard: A personalized page for each Doctor to view today's birthdays. Other tabs include Messages, Appointments and Usage- all of which are just dummy tabs and also the nav-bar items- Home, About, Projects, Contact.
  - Birthdays Today tab shows the list of all patient's who have a birthday on the current day according to US/Pacific time zone.
  - User gets the option to select the patients he/she wants to wish provided they have their email ids stored in the drchrono database.
  - User can add a subject or even leave it blank, in which case the default subject message would be used, i.e. "Happy Birthday from Dr. X" (PS: 'X' is the last name of the doctor).
  - User can customize the email message. The default message is - "Hi, Many Many Happy Returns of the day! We would like you to know that your next check-up is on us. Book your appointment today! :) - DrChrono team".
  - User can even discard these above changes and chose not to send any email or change his selected patient's list.
  - On submitting, an email is sent to all the selected patients instantaneously.
  - Since this is a mass email sending, the recipient list is added in the bcc, just to make things look more personalized from the patient's perspective.
  - Finally the User can logout, for security reasons ofcourse. :)  


Demo video url - https://youtu.be/ExtSmiS2ppU
