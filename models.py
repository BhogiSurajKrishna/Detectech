from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	username = models.CharField('username', max_length=255, blank=True,
								null=False)
	email = models.EmailField('email address', unique=True)
	states = models.IntegerField()
    # first_name = models.CharField('First Name', max_length=255, blank=True,
    #                               null=False)
    # last_name = models.CharField('Last Name', max_length=255, blank=True,
    #                              null=False)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return f"{self.email} - {self.username}"

class Client(models.Model):
	user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
	name = models.CharField(max_length=40)
	location = models.CharField(max_length=100)
