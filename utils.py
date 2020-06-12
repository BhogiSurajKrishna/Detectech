from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model
def get_and_authenticate_user(email, password):
	user = authenticate(username=email, password=password)
    #user=None if no user with those credentials exist
	if user is None:
		raise serializers.ValidationError("Invalid username/password. Please try again!")
	return user

def create_user_account(email, password,username):
	user = get_user_model().objects.create_user(email=email, password=password,username=username)
	return user