from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings
import insta
from insta import InstaMine
from models import Account
from manager import Provider as pd
from manager import LoginManager as lm
from manager import FetchManager as fm
from django.contrib.auth.decorators import login_required


import json

def index(request):
	print request
	print request.user
	"""
	Show initial document to user
	"""
	user = Account.objects.all()
	if len(user) != 1:
		return HttpResponseRedirect('/account_setup')
	context = RequestContext(request, {
									'sometext': settings.STATIC_URL,
									'instagram_url': '/redirect_url'
									})
	template = loader.get_template('dist/index.html')
	return HttpResponse(template.render(context))





def process_setup(request):
	context = RequestContext(request, {
									'sometext': settings.STATIC_URL,
									'instagram_url': '/redirect_url'
									})
	template = loader.get_template('app/views/process_setup.html')
	return HttpResponse(template.render(context))

def account_setup(request):
	"""
	Let user login here and get token
	"""
	return HttpResponse('<a href="/redirect_url">Setup your account here</a>')


def get_snaps(self):
	"""
	For Ajax, will grab media from database and send back json
	"""
	pass

# def login(request):
# 	# get the code and redirect user to instagram
# 	login_json_data = JSON.stringify({'login': true, 'posts_status': 'fetching'});
# 	code = request.Get.get('code', False)
# 	if not code:
# 		return HttpResponseRedirect(insta.INSTA_URL)
# 	else:
# 		api = InstaMine(request = request)
# 		if api.authenticate_user(code):
# 			return api.flow_manager()

# def init_fetch(request):
# 	#TODO: initiate fetching here
# 	#client will just poke
# 	#check login
# 	#fetch data
# 	if api.db_check_user(): #this function will check if token and user both are there
# 		api.get_snaps()
# 	pass

def get_update(request):
	#TODO: if user is logged in, return fetching
	# else return login false
	if api.db_check_user():

		fetching_status = api.db_fetch_status() #check from database the level of fetching
		if fetching_status.status == 'fetching':
			return {'login': True, 'posts_status': 'fetching'}
		elif fetching_status.status == 'done':
			return {'login': True, 'posts_status': 'done', 'progress': 100}
	else:
		return {'login': False}


def fetch(request):
	print 'here'
	#TODO: Check token here
	#get username

	last_id = request.GET.get('last_id', None)
	action = request.GET.get('fetch', False) or 'fetch' #remove after or
	username = 'arslanrafique'

	if action == 'fetch':
		return pd.fetch_update_posts(username = username, last_id = last_id)
	else:
		return pd.troll()

def update(request):
	#check for posts
	# if found posts return it
	# if no posts then check account
	# if no account then send no account response

	## ---- Get last id and return posts
	# request.post.get('')
	##

	# fm.fetch_posts(username='arslanrafique')
	last_id = None
	resp = pd.get_posts(last_id = last_id)
	if resp:
		return resp

def login(request):
	resp = lm.login(request = request)
	return resp
	#return HttpResponse(json.dumps({'test': False}))

def login_redirect(request):
	code = request.GET.get('code', False)


	if not code:
		return HttpResponseRedirect(insta.INSTA_URL)
	else:
		#show a page first and then execute below

		api = InstaMine(request=request)
		if api.authenticate_user(code):
			request_result = api.flow_manager()
			return HttpResponse(request_result, content_type="application/json")
			result = api.get_snaps()
	return HttpResponse(result or 'Got it')









