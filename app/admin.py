from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
	fields = ['date_published', 'title']

admin.site.register(Post, PostAdmin)
