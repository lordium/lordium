from django.http import HttpResponse, HttpResponseRedirect
from django.utils import six
from django.apps import apps
from django.utils.text import capfirst
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, NoReverseMatch
from app.models import Account, Post, GlobalConf
from datetime import datetime

# from django.contrib.admin.templatetags.admin_list
def make_time(f_time):
	if not f_time:
		return False
	today = datetime.now().date()
	if f_time.date() == today:
		return "Today"

	delta = today - f_time.date()
	if delta.days > 1:
		return str(delta.days) + ' days ago'
	else:
		return str(delta.days) + ' day ago'
	return f_time.date

def dashboard_front_data():
	try:
		config = GlobalConf.objects.get()
		accounts = config.total_accounts or '0'
		posts = config.total_posts or '0'
		date_fetched = make_time(config.last_fetched) or '0-0-0'
	except:
		accounts = '0'
		posts = '0'
		date_fetched = '0-0-0'



	return {'accounts':accounts , 'posts': posts, 'date_fetched': date_fetched}

class SuperAdmin(AdminSite):
	# @never_cache
	# def index(self, request, extra_context=None):
	# 	print 'login called'
	# 	return HttpResponseRedirect('/login')

	def login(self, request, extra_context=None):
		print request.user.is_authenticated()
		# print request.user.profile_picture
		print 'picture above'
		if not request.user.is_authenticated() or \
			not request.user.is_staff or \
			not request.user.is_active:
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
		index_response.context_data['active_dashboard_class'] = 'active'
		index_response.context_data['dashboard_front_data'] = dashboard_front_data()

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
		app_index_response.context_data['active_dashboard_class'] = 'active'
		return app_index_response


	def get_app_list(self, request):
		"""
		Its from the index function, new Django have this function
		"""
		app_dict = {}
		user = request.user
		for model, model_admin in self._registry.items():
			app_label = model._meta.app_label
			has_module_perms = user.has_module_perms(app_label)

			if has_module_perms:
				perms = model_admin.get_model_perms(request)

				# Check whether user has any perm for this module.
				# If so, add the module to the model_list.
				if True in perms.values():
					info = (app_label, model._meta.model_name)
					model_dict = {
						'name': capfirst(model._meta.verbose_name_plural),
						'object_name': model._meta.object_name,
						'perms': perms,
					}
					if perms.get('change', False):
						try:
							model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
						except NoReverseMatch:
							pass
					if perms.get('add', False):
						try:
							model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
						except NoReverseMatch:
							pass
					if app_label in app_dict:
						app_dict[app_label]['models'].append(model_dict)
					else:
						app_dict[app_label] = {
							'name': apps.get_app_config(app_label).verbose_name,
							'app_label': app_label,
							'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=self.name),
							'has_module_perms': has_module_perms,
							'models': [model_dict],
						}

		# Sort the apps alphabetically.
		app_list = list(six.itervalues(app_dict))
		app_list.sort(key=lambda x: x['name'].lower())

		# Sort the models alphabetically within each app.
		for app in app_list:
			app['models'].sort(key=lambda x: x['name'])

		return app_list



site = SuperAdmin()
site.disable_action('delete_selected')