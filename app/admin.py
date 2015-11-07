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
	list_display_links = None

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
		change_list_resp.context_data['app_list'] = app.site.index(request,
			extra_context = extra_context).context_data.get('app_list')
		change_list_resp.context_data['super_user'] = super_user
		change_list_resp.context_data['super_active_class'] = 'Posts'
		return change_list_resp


class AccountAdmin(admin.ModelAdmin):

	fields = ['username']

	list_display = ('account_image','username', 'first_name','fetch_status')

	list_per_page = 20

	def changelist_view(self, request, extra_context=None):
		super_user={}
		if request.user:
			try:
				super_user = Account.objects.get(username=request.user.username)
			except:
				pass
		change_list_resp = super(AccountAdmin, self).changelist_view(request, extra_context = extra_context)
		change_list_resp.context_data['app_list'] = app.site.index(request,
			extra_context = extra_context).context_data.get('app_list')
		change_list_resp.context_data['super_user'] = super_user
		change_list_resp.context_data['super_active_class'] = 'Accounts'
		print change_list_resp.context_data['cl']
		return change_list_resp





app.site.register(Post, PostAdmin)
app.site.register(Account, AccountAdmin)