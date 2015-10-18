from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^redirect_url/', views.login_redirect, name = 'login_redirect'),
	url(r'^account_setup/', views.account_setup, name = 'account_setup'),
	url(r'^process_setup/', views.process_setup, name = 'process_setup'),
]