from django.contrib import admin

# Register your models here.
from .models import Post, Account
import app

class PostAdmin(admin.ModelAdmin):
	fields = ['date_published', 'title']

	list_display = ('super_post_url', 'description', 'account')

	list_per_page = 20


class AccountAdmin(admin.ModelAdmin):

	fields = ['username']

	list_display = ('account_image','username', 'first_name')

	list_per_page = 20

app.site.register(Post, PostAdmin)
app.site.register(Account, AccountAdmin)
print 'Register called'
