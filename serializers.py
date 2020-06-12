from django.contrib.auth import get_user_model,password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=300, required=True)
	password = serializers.CharField(required=True, write_only=True)
	

class ForgotPassSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=300, required=True)
	# def validate_email(self, value):
	# 	user = User.objects.filter(email=value)
	# 	if not user:
	# 		raise serializers.ValidationError("Email doesn't exist")

class AuthUserSerializer(serializers.ModelSerializer):
	auth_token = serializers.SerializerMethodField()
#MethodField - can be dynamically generated by get_auth_token
	class Meta:
		model = User
		fields = ('id', 'email', 'username', 'is_active', 'is_staff','auth_token')
		read_only_fields = ('id', 'is_active', 'is_staff')
    
	def get_auth_token(self, obj):
		token = Token.objects.create(user=obj)
		return token.key

class EmptySerializer(serializers.Serializer):
	pass

class UserRegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email', 'username')
		#write_only_fields = ('password',)
		#read_only_fields = ('id',)

	def validate_email(self, value):
		user = User.objects.filter(email=value)
		if user:
			raise serializers.ValidationError("Email is already taken")
		return BaseUserManager.normalize_email(value)

	# def validate_password(self, value):
	# 	password_validation.validate_password(value)
	# 	return value

class PasswordChangeSerializer(serializers.Serializer):
	current_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	def validate_current_password(self, value):
		if not self.context['request'].user.check_password(value):
			raise serializers.ValidationError('Current password does not match')
		return value

	def validate_new_password(self, value):
		password_validation.validate_password(value)
		return value

class GeneralSerializer(serializers.ModelSerializer):
	#auth_token = serializers.SerializerMethodField()
#MethodField - can be dynamically generated by get_auth_token
	class Meta:
		model = User
		fields = ('id', 'email', 'username', 'is_active', 'is_staff')
		read_only_fields = ('id', 'is_active', 'is_staff')
    
	# def get_auth_token(self, obj):
	# 	token = Token.objects.create(user=obj)
	# 	return token.key