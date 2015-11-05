from superadmin import SuperAdmin, site

from django.utils.module_loading import autodiscover_modules

def autodiscover():
	print 'discovered'
	autodiscover_modules('admin', register_to=site)