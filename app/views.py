from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader

from django.conf import settings
import insta
from insta import InstaMine
from models import Account
from manager import Provider as pd
from forms import InitForm


import json

def index(request):
	# print request
	# print request.user
	"""
	Show initial document to user
	"""
	#


	context = RequestContext(request, {
									# 'sometext': settings.STATIC_URL,
									# 'instagram_url': '/redirect_url'
									})
	template = loader.get_template('dist/index.html')
	return HttpResponse(template.render(context))

def initiate_app(request):
	print request
	if request.POST:
		website_url = request.POST.get('website_url')
		client_id = request.POST.get('client_id')
		client_secret = request.POST.get('client_secret')
		if website_url and client_id and client_secret:
			pd.db_init_app(client_id, client_secret, website_url)

		website_redirect = website_url + '/redirect_url/'
		INSTA_URL = """https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code"""%(client_id, website_redirect)
		print INSTA_URL
		return HttpResponseRedirect(INSTA_URL)
	else:
		form = InitForm()
	return render(request, 'app/index.html', {'form': form})

@login_required(login_url='/')
def fetch(request):

	last_id = request.POST.get('last_id', None)
	action = request.POST.get('fetch', False) or 'fetch' #remove after or

	if hasattr(request,'user') and request.user.is_authenticated():
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
	code = request.GET.get('code', False)
	client_id = request.GET.get('client_id2', False)
	if code and client_id: #app config request
		pd.activate_app()
	resp = pd.login(request = request)
	return resp


def logout(request):
	return pd.logout(request)

def user_post(request):
	post_id = request.Get.get('post_id')
	if not post_id:
		return HttpResponseRedirect('/')
	return pd.logout(request)



