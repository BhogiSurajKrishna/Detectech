from django.urls import path,include
#from rest_framework import routers
#from .views import AuthViewSet
from .views import loginAPIView,registerAPIView,logoutAPIView,changepassAPIView,forgotpassAPIView,generalAPIView,create_clientAPIView
# router = routers.DefaultRouter()
# router.register('', AuthViewSet, basename='auth')

# urlpatterns = [
# 	path('',include(router.urls)),
# 	#path('rest-auth/', include('rest_auth.urls')),
# ]
app_name = 'accounts'

urlpatterns = [
	path('login/',loginAPIView.as_view(),name='login'),
	path('register/',registerAPIView.as_view(),name='register'),
	path('logout/',logoutAPIView.as_view(),name='logout'),
	path('changepass/',changepassAPIView.as_view(),name='changepass'),
	path('forgotpass/',forgotpassAPIView.as_view(),name='forgotpass'),
	path('general/',generalAPIView.as_view(),name='general'),
	path('cre_client/',create_clientAPIView.as_view(),name='cre_client'),
	#path('cre_section/',create_sectionAPIView.as_view(),name='cre_section'),

]
#RiuRxJHqCeWzf1bGG7fy2jMPamyVsu5GfjbzlIja - AWS secret access key
#user - suraj_s3_user
#group - django-s3-assets
#access key id - AKIATTY4JZW5MPCSAK3I
