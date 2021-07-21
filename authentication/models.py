from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from wagtail.core.models import Page
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class Zone(models.Model):
	zone = models.CharField(max_length = 100)

	def __str__(self):
		return self.zone

class State(models.Model):
	state = models.CharField(max_length = 100)

	def __str__(self):
		return self.state

class Region(models.Model):
	region = models.CharField(max_length = 100)

	def __str__(self):
		return self.region

class Divison(models.Model):
	divison = models.CharField(max_length = 100)

	def __str__(self):
		return self.divison

class District(models.Model):
	district = models.CharField(max_length = 100)

	def __str__(self):
		return self.district

class Mandal(models.Model):
	mandal = models.CharField(max_length = 100)

	def __str__(self):
		return self.mandal

class Village(models.Model):
	village = models.CharField(max_length = 100)

	def __str__(self):
		return self.village

class Dependent(models.Model):
	zone = models.ForeignKey(Zone, on_delete = models.CASCADE,blank = True,null = True)
	state = models.ForeignKey(State, on_delete = models.CASCADE, blank = True,null = True)
	region = models.ForeignKey(Region, on_delete = models.CASCADE, blank = True,null = True)
	divison = models.ForeignKey(Divison, on_delete = models.CASCADE, blank = True,null = True)
	district = models.ForeignKey(District, on_delete = models.CASCADE, blank = True,null = True)
	mandal = models.ForeignKey(Mandal, on_delete = models.CASCADE, blank = True,null = True)
	village = models.ForeignKey(Village, on_delete = models.CASCADE, blank = True,null = True)

	class Meta:
		abstract = True

class UserType(models.Model):
	usertype = models.CharField(max_length = 100)

	def __str__(self):
		return self.usertype

class Company(models.Model):
	company = models.CharField(max_length = 100)

	def __str__(self):
		return self.company

	class Meta:
		verbose_name = "Company"
		verbose_name_plural = "Companies"

class MyUser(AbstractUser,Dependent):

	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        db_index=True, primary_key=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },)
	company = models.ForeignKey(Company, on_delete = models.CASCADE,blank = True,null = True)
	usertype = models.ForeignKey(UserType, on_delete = models.CASCADE,blank = True,null = True)
	address = models.TextField(blank = True,null = True)
	mobile = PhoneNumberField(blank = True,null = True)
	officer = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete = models.SET_NULL , null = True, blank = True)

	REQUIRED_FIELDS = ['email']




