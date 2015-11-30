from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from models import Account
from manager import Provider as pd
from forms import InitForm

import json

def index(request, post_id=None, post_title=None):
	"""
	Show initial document to user
	"""
	req_context = {}
	config = pd.get_config()
	if not config or config.insta_connected == False:
		return HttpResponseRedirect('/init_app')

	req_context['google_analytics'] = config.google_analytics or ''
	req_context['description'] = config.description or ''
	req_context['title'] = config.title or ''

	if post_id and post_id > 0:
		post_data = pd.db_get_single(post_id=post_id)
		req_context['direct_post'] = post_data

	context = RequestContext(request, req_context)
	template = loader.get_template('dist/index.html')
	return HttpResponse(template.render(context))

def initiate_app(request):
	conf = pd.get_config()
	if conf and conf.insta_connected == True:
		return HttpResponseRedirect('/')
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
	if request.method =="POST":
		last_id = request.POST.get('last_id', None)
		action = request.POST.get('fetch', False) or 'fetch' #remove after or
		if action!= 'fetch':
			return HttpResponseRedirect('/')
		if hasattr(request,'user') and request.user.is_authenticated():
			if action == 'fetch':
				if request.user:
					return pd.fetch_update_posts(username = request.user, last_id = last_id)
	return HttpResponseRedirect('/')

@csrf_exempt
def update(request):
	if request.method == "POST":
		if request.body:
			data = json.loads(request.body)
			flag =  data.get('flag')
			if not flag:
				return HttpResponseRedirect('/')
			last_id = data.get('last_id', None)
			resp = pd.get_posts(last_id = last_id, request = request)
			if resp:
				return resp
	return HttpResponseRedirect('/')

def login(request):
	code = request.GET.get('code', False)
	if code: #app config request
		pd.activate_app()
	resp = pd.login(request = request)
	return resp


def logout(request):
	return pd.logout(request)



