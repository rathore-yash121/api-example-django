from django import forms

# forms go here

#birthdayEmail form to capture the message
class BirthdayEmail(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=800)
