from django.contrib.auth import get_user_model,logout,login
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status,generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserLoginSerializer,AuthUserSerializer,EmptySerializer,UserRegistrationSerializer,PasswordChangeSerializer,ForgotPassSerializer,GeneralSerializer,ClientSerializer
from .utils import get_and_authenticate_user,create_user_account
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
#import pdb
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import models
import random
import string
a = [i for i in string.ascii_letters]
b = ['0','1','2','3','4','5','6','7','8','9']
c = ['@','#','$','&']
d = a + b + c

User = get_user_model()






class loginAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = UserLoginSerializer
	def post(self,request):
		# if request.user:
		# 	print(request.user)
			#return redirect('/general/')
		logins = self.get_serializer(data = request.data)
		if logins.is_valid():
			user = get_and_authenticate_user(**logins.validated_data)
			if user:
				login(request,user)
			token = Token.objects.filter(user = request.user)
			if token:
				return redirect('/general/')
			serializer1 = AuthUserSerializer(user)
			f = serializer1.data
			if user.states == 1:
				user.states = 0
				user.save()
				return redirect('/changepass/')
			#print(request.user)
			#return Response(serializer1.data)
			return redirect('/general/')
		return Response({'error':'give correct fields'})

class generalAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = GeneralSerializer
	def get(self,request):
		print(request.user)
		if request.user.is_anonymous:
			data = {'Empty': 'No user logged in'}
			return Response(data=data)
		token = Token.objects.filter(user=request.user)
		if not token:
			logout(request)
			data = {'Empty': 'No user logged in'}
			return Response(data=data)
		serializer = self.get_serializer(request.user)
		#print(request.user)
		login(request,request.user)
		#token = Token.objects.filter(user=request.user)
		# if token:
		# 	print(token[0].key)
		#print(serializer.data)
		diction = serializer.data
		if token:
			diction['token'] = token[0].key
		return Response(diction)

class registerAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = UserRegistrationSerializer
	def post(self,request):
		registers = self.get_serializer(data=request.data)
		if registers.is_valid():
			p = ''.join(random.choice(d) for i in range(12))
			m = registers.validated_data['email']
			user = User.objects.create_user(
        		email=registers.validated_data['email'], password=str(p),username=registers.validated_data['username'],states=1)
			#user.states=1
			send_mail(
			'Dummy Password for your first login',
			'Your dummy password for your first login is ' + str(p) + ' please change it.',
			'surajbogi295@gmail.com',
			[m],
			fail_silently=False)
			return Response({'Hurray':'Your registraton is successful,you can login now with password sent to your mail'})
		return Response({'error':'give correct fields'})

#@login_required
class logoutAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = UserLoginSerializer
	#@login_required
	def get(self,request):
		if request.user.is_anonymous:
			data = {'Empty': 'No user logged in'}
			return Response(data=data)
		token = Token.objects.filter(user = request.user)
		if token:
			token[0].delete()
			logout(request)
			data = {'success':'Succesful'}
			return Response(data=data)
		else:
			logout(request)
			print(request.user)
			data = {'Empty': 'No user logged in'}
			return Response(data=data)

#@login_required
class changepassAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = PasswordChangeSerializer
	#@login_required
	def post(self,request):
		if request.user.is_anonymous:
			data = {'Empty': 'No user logged in'}
			return Response(data=data)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		#login(request,request.user)
		request.user.set_password(serializer.validated_data['new_password'])
		request.user.save()
		login(request,request.user)
		#return Response({'OK':'Password changed successfully'})
		return redirect('/general/')
class forgotpassAPIView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = ForgotPassSerializer
	def post(self,request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		#print(serializer.validated_data['email'])
		mail = serializer.validated_data['email']
		user = User.objects.filter(email=serializer.validated_data['email']).first()
		p = ''.join(random.choice(d) for i in range(12))
		if user:
			send_mail(
			'Password Change',
			'Your dummy password is' + str(p) + ' please change it.',
			'surajbogi295@gmail.com',
			[mail],
			fail_silently=False)
			user.set_password(str(p))
			user.save()
			return Response({'Ok':'We have sent an email of dummy password'})
		return Response({'false_validity': 'not valid email or email doesnt exist'})



class create_clientAPIView(generics.GenericAPIView):
	#authentication_classes = [TokenAuthentication,]
	#permission_classes = [IsAuthenticated,]
	queryset = User.objects.all()
	serializer_class = ClientSerializer
	def post(self,request):
		data = {'Empty': 'No user logged in'}
		if request.user.is_anonymous:
			return Response(data=data)
		token = Token.objects.filter(user = request.user)
		if not token:
			return Response(data=data)
		client = models.Client.objects.filter(user=request.user)
		if client:
			data = {'Disallowed': 'You are already registered as a client'}
			return Response(data)
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			models.Client.objects.create(user=request.user,name=serializer.validated_data['name'],location=serializer.validated_data['location'])
			return redirect('/general/')
	def get(self,request):
		data = {'Empty': 'No user logged in'}
		if request.user.is_anonymous:
			return Response(data=data)
		token = Token.objects.filter(user = request.user)
		if not token:
			return Response(data=data)
		client = models.Client.objects.filter(user=request.user)
		if not client:
			data = {'Empty': 'You have no client registered'}
			return Response(data)
		serializer = self.get_serializer(client[0])
		return Response(serializer.data)
	# def put(self,request):
	# 	data = {'Empty': 'No user logged in'}
	# 	if request.user.is_anonymous:
	# 		return Response(data=data)
	# 	token = Token.objects.filter(user = request.user)
	# 	if not token:
	# 		return Response(data=data)
	# 	client = models.Client.objects.filter(user=request.user)
	# 	if not client:
	# 		data = {'Empty': 'You have no client registered'}
	# 		return Response(data)
		

# class create_sectionAPIView(generics.GenericAPIView):
# 	queryset = Client.objects.all()
# 	serializer_class = SectionSerializer
# 	def post(self,request):
