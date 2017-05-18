from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
# Create your models here.

@python_2_unicode_compatible
class PatientDataModel(models.Model):
    patient_id = models.IntegerField(null=False, primary_key=True)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    doctor_id = models.IntegerField(null=False)
    birthday = models.DateField(default=datetime.date)
    patient_email = models.EmailField(default="")

    def __str__(self):
        hyphen = "|"
        patient = (str(self.patient_id),self.first_name,self.last_name,str(self.birthday),str(self.patient_email))
        return hyphen.join(patient)
