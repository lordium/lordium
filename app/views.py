from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.conf import settings
import insta
from insta import InstaMine
from models import Account

def index(request):
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


def login_redirect(request):
	code = request.GET.get('code', False)

	if not code:
		return HttpResponseRedirect(insta.INSTA_URL)
	else:
		#show a page first and then execute below

		api = InstaMine(request=request)
		if api.authenticate_user(code):
			api.flow_manager()
			result = api.get_snaps()
	return HttpResponse(result or 'Got it')

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







