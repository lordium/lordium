from django.http import HttpResponse, HttpResponseRedirect
from django.utils import six
from django.apps import apps
from django.utils.text import capfirst
from django.contrib.admin import AdminSite,ModelAdmin
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, NoReverseMatch
from app.models import Account

class SuperAdmin(AdminSite):
	# @never_cache
	# def index(self, request, extra_context=None):
	# 	print 'login called'
	# 	return HttpResponseRedirect('/login')

	def login(self, request, extra_context=None):
		print request.user.is_authenticated()
		print request.user.profile_picture
		print 'picture above'
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/login')
		return super(SuperAdmin, self).login(request, extra_context=extra_context)

	@never_cache
	def index(self, request, extra_context=None):
		index_response = super(SuperAdmin, self).index(request, extra_context)
		user = index_response.context_data.get('user', False)
		if not user:
			user = request.user or False
		super_user = False
		if user:
			try:
				super_user = Account.objects.get(username=user.username)
			except:
				pass
		if super_user:
			index_response.context_data['super_user'] = super_user

		return index_response

	def app_index(self, request, app_label, extra_context=None):
		app_index_response = super(SuperAdmin, self).app_index(request,
			app_label, extra_context = extra_context)
		user = app_index_response.context_data.get('user', False)
		if not user:
			user = request.user or False
		super_user = False
		if user:
			try:
				super_user = Account.objects.get(username=user.username)
			except:
				pass
		if super_user:
			app_index_response.context_data['super_user'] = super_user

		return app_index_response


class SuperBaseModelAdmin(ModelAdmin):

    def changelist_view(self, request, extra_context=None):
    	change_list_resp = super(SuperBaseModelAdmin, self).changelist_view(request, extra_context = extra_context)
    	change_list_resp.context_data['testtest'] = 'yahoo'
    	print 'sadfasdfasd'
    	return change_list_resp
    	return {}



site = SuperAdmin()