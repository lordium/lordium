from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings
import insta
from insta import InstaMine
from models import Account
from manager import Provider as pd


import json

def index(request):
	# print request
	# print request.user
	"""
	Show initial document to user
	"""

	print request.user
	# user = Account.objects.all()
	# if len(user) != 1:
	# 	return HttpResponseRedirect('/login')
	context = RequestContext(request, {
									# 'sometext': settings.STATIC_URL,
									# 'instagram_url': '/redirect_url'
									})
	template = loader.get_template('dist/index.html')
	return HttpResponse(template.render(context))

def fetch(request):
	print 'here'
	#TODO: Check token here
	#get username

	last_id = request.GET.get('last_id', None)
	action = request.GET.get('fetch', False) or 'fetch' #remove after or
	username = 'arslanrafique'
	if request.user.is_authenticated():
		if action == 'fetch':
			if request.user:
				return pd.fetch_update_posts(username = request.user, last_id = last_id)
	return pd.troll()

def update(request):
	last_id = request.GET.get('last_id', None)
	resp = pd.get_posts(last_id = last_id, request = request)
	# print request.user.is_authenticated()
	# print resp
	if resp:
		return resp

def login(request):
	resp = pd.login(request = request)
	return resp


def logout(request):
	return pd.logout(request)

def user_post(request):
	post_id = request.Get.get('post_id')
	if not post_id:
		return HttpResponseRedirect('/')
	return pd.logout(request)



