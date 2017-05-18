from django import forms

# forms go here
class BirthdayEmail(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=800)
