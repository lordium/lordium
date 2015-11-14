from django.contrib import admin

# Register your models here.
from .models import Post, Account, GlobalConf
import app
from django.http import HttpResponse, HttpResponseRedirect

from django import forms
from django.utils.translation import ugettext_lazy as _

class SuperActionForm(forms.Form):
    action = forms.ChoiceField(label='Actions')
    select_across = forms.BooleanField(label='', required=False, initial=0,
        widget=forms.HiddenInput({'class': 'select-across form-control'}))


class PostAdmin(admin.ModelAdmin):

	readonly_fields = ('title', 'description', 'date_published',
		'account','location_name')
	fields = ['title',
		'description',
		'date_published',
		'location_name',
		'account']

	list_display = ('super_post_url', 'account')

	list_per_page = 20

	# actions_selection_counter = False
	# list_display_links = None

	max_num = 0

	action_form = SuperActionForm

	def get_readonly_fields(self, request, obj=None):
		fields = self.readonly_fields
		# if obj:
		# 	fields = fields + ('username',)
		# if Account.objects.get(username=request.user.username).read_only:
		# 	fields = fields + ('read_only','is_active', 'fetch_status')
		return fields

	def get_actions(self, request):
		actions = super(PostAdmin, self).get_actions(request)
		if Account.objects.get(username=request.user.username).read_only:
			del actions['delete_selected']
		return actions

	def has_delete_permission(self, request, obj=None):
		perm = super(PostAdmin, self).has_delete_permission(request, obj = obj)
		if Account.objects.get(username=request.user.username).read_only:
			return False
		return perm

	def has_add_permission(self, request):
		return False

	def changelist_view(self, request, extra_context=None):
		super_user={}
		if request.user:
			try:
				super_user = Account.objects.get(username=request.user.username)
			except:
				pass
		change_list_resp = super(PostAdmin, self).changelist_view(request, extra_context = extra_context)
		if hasattr(change_list_resp, 'context_data'):
			change_list_resp.context_data['app_list'] = app.site.get_app_list(request)
			change_list_resp.context_data['super_user'] = super_user
			change_list_resp.context_data['super_active_class'] = 'Posts'
		return change_list_resp


	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		render_response = super(PostAdmin, self).render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)
		if hasattr(render_response, 'context_data'):
			render_response.context_data['app_list'] = app.site.get_app_list(request)
			render_response.context_data['super_active_class'] = 'Posts'
		return render_response




class AccountAdmin(admin.ModelAdmin):

	# readonly_fields = ('fetch_status',)

	# fields = ('username','is_active','fetch_status')

	fieldsets = (
		('Account', {
				'fields': ('username', 'is_active', 'fetch_status', 'read_only'),
				'description': 'Account is used to fetch posts from Instagram',
				'classes':('panel','col-xs-12 col-sm-12 col-md-12 col-lg-12')
			}),
		)

	list_display = ('account_image','username', 'first_name','fetch_status')

	list_per_page = 20

	# def __init__(self, *args, **kwargs):
	# 	# self.the_app_list = app.site.index().context_data.get('app_list')
	# 	return super(AccountAdmin, self).__init__(*args, **kwargs)

	def get_actions(self, request):
		actions = super(AccountAdmin, self).get_actions(request)
		if Account.objects.get(username=request.user.username).read_only:
			del actions['delete_selected']
		return actions

	def has_delete_permission(self, request, obj=None):
		perm = super(AccountAdmin, self).has_delete_permission(request, obj = obj)
		if Account.objects.get(username=request.user.username).read_only:
			return False
		return perm

	def has_add_permission(self, request):
		perm = super(AccountAdmin, self).has_add_permission(request)
		if Account.objects.get(username=request.user.username).read_only:
			return False
		return perm

	def get_readonly_fields(self, request, obj=None):
		fields = self.readonly_fields
		if obj:
			fields = fields + ('username',)
		if Account.objects.get(username=request.user.username).read_only:
			fields = fields + ('read_only','is_active', 'fetch_status')
		return fields

	def changelist_view(self, request, extra_context=None):
		super_user={}
		if request.user:
			try:
				super_user = Account.objects.get(username=request.user.username)
			except:
				pass
		change_list_resp = super(AccountAdmin, self).changelist_view(request, extra_context = extra_context)
		if hasattr(change_list_resp, 'context_data'):
			change_list_resp.context_data['app_list'] = app.site.get_app_list(request)
			change_list_resp.context_data['super_user'] = super_user
			change_list_resp.context_data['super_active_class'] = 'Accounts'
		return change_list_resp

	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		render_response = super(AccountAdmin, self).render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)
		if hasattr(render_response, 'context_data'):
			render_response.context_data['app_list'] = app.site.get_app_list(request)
			render_response.context_data['super_active_class'] = 'Accounts'
		return render_response


class ConfAdmin(admin.ModelAdmin):
	fieldsets = (
		('Settings', {
				'fields': ('instagram_app_id','instagram_app_secret',
					'google_analytics'),
				'description': 'Add your apps detail',
				'classes':('panel','col-xs-12 col-sm-12 col-md-12 col-lg-12')
			}),
		)

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(ConfAdmin, self).get_actions(request)
		del actions['delete_selected']
		return actions

	def changelist_view(self, request, extra_context=None):
		return HttpResponseRedirect('/dashboard/app/globalconf/1/')

		super_user={}
		if request.user:
			try:
				super_user = Account.objects.get(username=request.user.username)
			except:
				pass
		change_list_resp = super(ConfAdmin, self).changelist_view(request, extra_context = extra_context)
		if hasattr(change_list_resp, 'context_data'):
			change_list_resp.context_data['app_list'] = app.site.get_app_list(request)
			change_list_resp.context_data['super_user'] = super_user
			change_list_resp.context_data['super_active_class'] = 'Settings'
		return change_list_resp

	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		render_response = super(ConfAdmin, self).render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)
		if hasattr(render_response, 'context_data'):
			render_response.context_data['app_list'] = app.site.get_app_list(request)
			render_response.context_data['super_active_class'] = 'Settings'
		return render_response


# GlobalConf.get_config()
app.site.register(GlobalConf, ConfAdmin)
app.site.register(Post, PostAdmin)
app.site.register(Account, AccountAdmin)
