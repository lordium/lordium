from django.conf.urls import url
import views
import app

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	## instagram will redirect to following url
	url(r'^redirect_url/', views.login, name = 'login_redirect'),

	# url(r'^account_setup/', views.account_setup, name = 'account_setup'),
	# url(r'^process_setup/', views.process_setup, name = 'process_setup'),

	## will be responsible for getting snaps
	# url(r'^get_update/', views.get_update, name = 'get_update'),

	## will be responsible for telling if fetching completed or not
	# url(r'^login_status/', views.process_setup, name = 'login_status'),

	##user will be directed here and then to instagram
	# url(r'^login/', views.process_setup, name = 'login_status'),

	#######################################

	url(r'^update/', views.update, name = 'update'),

	##user will be directed here and then to instagram
	url(r'^login/', views.login, name = 'login'),

	url(r'^logout/', views.logout, name = 'logout'),

	##allow user to fetch data
	url(r'^fetch/', views.fetch, name = 'fetch'),

]

