from django.db import models
from datetime import datetime
from datetime import date, time
from django.db import models
from django.core.exceptions import ValidationError
import uuid

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)


class Voter(models.Model):
    Voter_Image = models.ImageField(upload_to="media/", height_field=None, width_field=None, max_length=100, null=True)
    Voter_id = models.CharField(max_length=5, primary_key=True)
    Name = models.CharField(max_length=50)
    Age = models.PositiveSmallIntegerField()
    Date_of_Birth = models.DateField(max_length=20, null=True)
    Gender = models.CharField(max_length=120, choices=GENDER_CHOICES, null=True)
    Phone_Number = models.IntegerField()
    Address = models.TextField(max_length=250)
    Address_Proof = models.ImageField(upload_to="media/", height_field=None, width_field=None, max_length=100,
                                      null=True)
    Iris_Image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True)
    Poling_Status = models.BooleanField(max_length=5, null=True)

    def clean(self):
        if self.Age < 18:
            raise ValidationError(
                {'Age': "You must be 18 years old"})

    def clean(self):
        dob = self.Date_of_Birth
        age = (date.today() - dob).days / 365
        if age < 18:
            raise ValidationError(
                {'Date_of_Birth': "You must be 18 years old"})

    def clean(self):
        if not len(str(self.Phone_Number)) == 10:
            raise ValidationError(
                {'Phone_Number': "Enter phone number in correct formate"})




class Add_Nominee(models.Model):
    Nominee_Id = models.CharField(max_length=100, unique=True, null=True)
    Nominee_Name = models.CharField(max_length=100)
    Nominee_Photo = models.ImageField(upload_to="media/nominee/", height_field=None, width_field=None)
    Party = models.CharField(max_length=100)
    Sign = models.ImageField(upload_to="media/nominee", height_field=None, width_field=None)

    def clean(self):
        if self.Nominee_Name.isdigit():
            raise ValidationError(
                {'Nominee_Name': "Enter characters only"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Votes(models.Model):
    Nominee_Id = models.ForeignKey(Add_Nominee, on_delete=models.CASCADE, null=True)
    Voter = models.ForeignKey(Voter, on_delete=models.CASCADE, null=True)
    Date = models.DateField()


class CreateElection(models.Model):
    Election_code = models.CharField(max_length=100)
    Election_Name = models.CharField(max_length=100)
    Election_Start_Date = models.DateTimeField()
    Election_End_Date = models.DateTimeField()
    Election_Result_Date = models.DateTimeField()

    def clean(self):
        erd = self.Election_Result_Date.date()
        if date.today() > self.Election_Start_Date.date():
            raise ValidationError(
                {'Election_Start_Date': "Choose correct date"})
        if date.today() > self.Election_End_Date.date():
            raise ValidationError(
                {'Election_End_Date': "Choose correct date"})
        if date.today() > erd:
            raise ValidationError(
                {'Election_Result_Date': "Choose correct date"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class last_login(models.Model):
    voter_id = models.CharField(max_length=10)


class Iris_model(models.Model):
    iris_image = models.ImageField(upload_to='media/Images')

class prediction(models.Model):
    predicted_label = models.PositiveIntegerField(null=True)

class voting_count(models.Model):
    Nominee_Id = models.ForeignKey(Add_Nominee, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
