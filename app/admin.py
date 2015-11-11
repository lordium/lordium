from django.contrib import admin

# Register your models here.
from .models import Post, Account
import app

from django import forms
from django.utils.translation import ugettext_lazy as _

class SuperActionForm(forms.Form):
    action = forms.ChoiceField(label='Actions')
    select_across = forms.BooleanField(label='', required=False, initial=0,
        widget=forms.HiddenInput({'class': 'select-across form-control'}))


class PostAdmin(admin.ModelAdmin):
	fields = ['date_published', 'title']

	list_display = ('super_post_url', 'account')

	list_per_page = 20

	# actions_selection_counter = False
	# list_display_links = None

	max_num = 0

	action_form = SuperActionForm

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

	def has_add_permission(self, request):
		return False




class AccountAdmin(admin.ModelAdmin):

	# readonly_fields = ('fetch_status',)

	# fields = ('username','is_active','fetch_status')

	fieldsets = (
		('Account', {
				'fields': ('username', 'is_active', 'fetch_status'),
				'description': 'Account is used to fetch posts from Instagram',
				'classes':('panel','col-xs-12 col-sm-12 col-md-12 col-lg-12')
			}),
		)

	# fieldsets = (
 #        (None, {
 #            'fields': ('url', 'title', 'content', 'sites')
 #        }),
 #        ('Advanced options', {
 #            'classes': ('collapse',),
 #            'fields': ('enable_comments', 'registration_required', 'template_name')
 #        }),
 #    )

	list_display = ('account_image','username', 'first_name','fetch_status')

	list_per_page = 20

	# def __init__(self, *args, **kwargs):
	# 	# self.the_app_list = app.site.index().context_data.get('app_list')
	# 	return super(AccountAdmin, self).__init__(*args, **kwargs)

	def get_actions(self, request):
		actions = super(AccountAdmin, self).get_actions(request)
		# if request.user.username[0].upper() != 'J':
		#     del actions['delete_selected']
		print actions
		return actions

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ('username',)
		return self.readonly_fields

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
		return render_response



app.site.register(Post, PostAdmin)
app.site.register(Account, AccountAdmin)