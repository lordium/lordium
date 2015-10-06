from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings

def index(request):
	context = RequestContext(request, {'sometext': settings.STATIC_URL})
	template = loader.get_template('dist/index.html')
	return HttpResponse(template.render(context))
