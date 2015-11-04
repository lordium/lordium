import json
import confs
import insta
import models
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login as db_login
from django.contrib.auth import logout as db_logout
from django.http import HttpResponse, HttpResponseRedirect

from darbaan.darbaan import Darbaan



# Below is utility function section
def response_wrapper(response_function):
	def inner(*args, **kwargs):
		data = response_function(*args, **kwargs)
		response = HttpResponse(json.dumps(data))
		## can use below as well
		#from django.http import JsonResponse
		#return JsonResponse({'foo':'bar'})
		#TODO: use below for error
		#response.status_code = 500
		return response
	return inner


class LoginManager(object):
	"""
	This manager is responsible for geting login signal from
	client, redirecting to external vendor, and fetching user
	access token, and managing it.
	"""


	@classmethod
	def login(self, request=None, vendor='insta'):
		"""
		Let the user login using vendor
		"""

		if request.user.is_authenticated():
			return ResponseManager.redirect('/')

		code = request.GET.get('code', False)

		if not request:
			return False

		if vendor and vendor == 'insta':
			if not code:
				return Darbaan.insta_redirect() #
			else:
				_api = Darbaan(request)
				user_info = _api.insta_login(code)
				if user_info:
					fetch_status = DBManager.check_account(username=user_info.get('username'))
					username = user_info.get('username')


					if fetch_status:
						#TODO: add session/cookies here
						# print request.session['access_token']
						# print fetch_status
						account_status = 'new_account'
						if fetch_status == 1:
							account_status = 'new_account'
						elif fetch_status == 2:
							account_status = 'fetching'
						elif fetch_status == 3:
							account_status = 'fetch_completed'
						print 'above auth'
						u_account = authenticate(username=username, password=username) #;)
						print u_account, username
						db_login(request, u_account)

						return ResponseManager.redirect('/') #simple_response({'login_status': True, 'account_status': account_status})
					else:
						if DBManager.db_create_account(user_info, request = request):
							#TODO: add session.cookies here

							# u = models.Account.objects.get(username = username)
							# print u
							# u.set_password(username)
							# u.save()

							u_account = authenticate(username=username, password=username) #;)
							print u_account
							db_login(request, u_account)
							return ResponseManager.redirect('/')# ({'login_status': True, 'account_status': 'new_account'})
						else:
							return ResponseManager.redirect('/')#
							# return ResponseManager.simple_response({'login_status': False, 'account_status': 'creation_failed'})
				return ResponseManager.redirect('/')#
				# return ResponseManager.simple_response({'login_status': False, 'account_status': 'permission_failed'})


	@classmethod
	# @response_wrapper
	def logout(self, request):
		db_logout(request)
		return ResponseManager.redirect('/')


class DBManager(object):
	"""
	This manager is only responsible for reading and writing
	data to database, it shouln't perform any computation
	related to logic
	"""
	@classmethod
	def check_account(self, vendor='insta', username = None):
		"""
		This will check if user already exists
		"""
		account = False
		try:
			account = models.Account.objects.get(username=username)
		except models.Account.DoesNotExist:
			account = False
		if account:
			return account.fetch_status
		return False


	@classmethod
	def db_create_account(self, user_info, request = None,  **kwargs):
		"""
		This function will create account and write it to
		database
		"""
		"""
		Below is what insta will give
		{
		u'username': u'arslanrafique',
		u'bio': u'Engineer, <3 Stockholm!',
		u'website': u'',
		u'profile_picture': u'https://scontent.cdninstagram.com/hphotos-xpf1/t51.2885-19/924761_778256512251267_1485306869_a.jpg',
		u'full_name': u'Arslan Rafique',
		u'id': u'1141033715'
		 }
		"""
		if request:
			print "username is", user_info.get('username')
			account = models.Account.create(username = user_info.get('username'),
											slogan = user_info.get('bio', ''),
											profile_picture = user_info.get('profile_picture'),
											first_name = user_info.get('full_name'),
											last_name=" ",
											email="example@example.com",
											insta_id = user_info.get('id'),
											insta_token = request.session['access_token'],
											fetch_status = 1)

			if account:
				return True
		return False


	@classmethod
	def db_last_id(self, account):
		try:
			latest = models.Post.objects.filter(account=account).latest('id').id
		except:
			latest = False
		return latest

	@classmethod
	def db_get_dirty_accounts(self):
		return models.Account.objects.filter(Q(fetch_status=1)|Q(fetch_status=4))

	@classmethod
	def delete_account(self):
		"""
		This function will delete account and all posts
		"""
		pass

	@classmethod
	def db_create_posts(self, posts, account_reference):
		"""
		This function will create new posts in database
		its going to be bulk function
		"""


		db_posts = []
		for post in posts:
			single_post = models.Post(
								media_id = post.get('media_id'),
								title = post.get('title', None),
								description = post.get('description', None),
								date_published = post.get('date_published'),
								post_type = post.get('post_type'),
								post_url = post.get('post_url'),
								post_tags = post.get('post_tags'),
								location = post.get('location'),
								location_name = post.get('location_name'),
								account = account_reference)

			db_posts.append(single_post)

		return models.Post.post_bulk_create(db_posts)

	@classmethod
	def get_token(self):
		"""
		This function will return user token for fetching
		data
		"""

	@classmethod
	def db_get_posts(self, last_id=None):
		"""
		This function will fetch posts from database
		"""
		final_result = False
		# posts = models.Post.objects.all()
		if last_id:
			posts = models.Post.objects.filter(id__gt=last_id).order_by('id')[:2]
		else:
			posts = models.Post.objects.order_by('id')[:2]
		if posts and len(posts) > 0:
			return posts
		return final_result



class CacheManager(object):
	"""
	This manager is responsible to get data from cache, if data
	is not present, then read it from database and update the
	cache before sending response back to user
	"""

	@classmethod
	def cache_get_posts(self, last_id=None):
		"""
		This function will fetch posts from cache
		"""
		pass

	@classmethod
	def cache_get_db(self, last_id=None):
		"""
		This function will get posts from DB and update the cache
		"""

	@classmethod
	def update_cache(self, posts=None):
		"""
		This function will get the posts and update the cache
		"""
	pass

class FetchManager(object):
	"""
	This manager is responsible for fetching data from vendors
	"""
	@classmethod
	def fm_fetch_posts(self, vendor='insta', username = None, last_id=None):
		"""
		This function will fetch posts from vendors
		"""
		if vendor and vendor == 'insta' and username:
			account = models.Account.objects.get(username=username)
			if account:
				token = account.insta_token
				return Darbaan.insta_fetch(token=token, last_id=last_id)
		return False

class ResponseManager(object):
	"""
	This class is responsible for construction and sending responses
	"""

	@classmethod
	def redirect(self, url,**kwargs):
		"""
		Redirect user but adding the kwargs
		"""
		#TODO: Add kwargs

		return HttpResponseRedirect(url)

	@classmethod
	def simple_response(self, data, make_json=True, **kwargs):
		if make_json:
			data = json.dumps(data)
		return HttpResponse(data)

class Provider(LoginManager, DBManager, FetchManager, ResponseManager):

	@classmethod
	@response_wrapper
	def get_posts(self, last_id=None, request=None):
		"""
		get posts, if not, check account,
		"""

		posts = self.db_get_posts(last_id = last_id)
		if posts:
			lucky_image = False
			brand_info = False
			if not last_id:
				accounts = models.Account.objects.all()
				if accounts and len(accounts) > 0:
					lucky_image = accounts[0].profile_picture
					if request and request.user.is_authenticated():
						brand_info = accounts[0].username #TODO: use session here

			return self.make_posts(posts, lucky_image, brand_info)
		else:
			accounts = models.Account.objects.all()
			#using account[0], first user will be king!
			if accounts and len(accounts) > 0:
				if accounts[0].fetch_status == 1: #1 => NEW
					return self.make_dict(True, 'no_posts', 'new_account')
				elif accounts[0].fetch_status == 2: #2 => Fetching
				 	return self.make_dict(True, 'no_posts', 'fetching')
				elif accounts[0].fetch_status == 3: #3 => Fetch Completed
					return self.make_dict(True, 'no_posts', 'fetch_completed')
			else:
				return self.make_dict(False, 'no_posts', 'no_account')


	@classmethod
	def make_dict(self, success=True, data_type=None, account_status=None):
		return {'success': success,
				'data_type': data_type,
				'account_status': account_status}

	@classmethod
	def make_posts(self, posts, lucky_image, brand_info):
		posts_dict = self.make_dict(True, 'posts', 'fetch_completed')
		posts_dict['lucky_image'] = lucky_image or None
		posts_dict['brand_info'] = brand_info or None
		posts_container = []
		for post in posts:
			posts_container.append({ 'title': post.title or None,
									 'type': post.post_type,
									 'id': post.id,
									 'img_url': post.post_url or None,
									 'description': post.description or None,
									 'location': post.location_name or None,
									 'post_type': post.post_type or None,
									 'tags': post.post_tags or None
									})


		posts_dict['posts'] = posts_container
		return posts_dict

	@classmethod
	def fetch_update_posts(self, vendor='insta', username=None, last_id = None):
		#TODO: get last data id from database
		#Get the accounts for dirty/new
		dirty_accounts = self.db_get_dirty_accounts()
		if dirty_accounts and len(dirty_accounts) > 0:
			for account in dirty_accounts:
				last_id = self.db_last_id(account) or None
				posts = self.fm_fetch_posts(vendor=vendor, username=account.username, last_id=last_id)
				if posts and self.db_create_posts(posts, account):
					account.fetch_status = 3
					account.save()
					return self.simple_response({'status': 'success', 'fetch_status': 'completed'})
		return self.simple_response({'status': 'failed', 'fetch_status': 'not_completed'})

	@classmethod
	def troll(self):
		return self.simple_response({'status': 'failed', 'fetch_status': 'not_completed'})

















