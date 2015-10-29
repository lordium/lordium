import models
import insta
from insta import InstaMine as _im
from django.http import HttpResponse, HttpResponseRedirect
from instagram.client import InstagramAPI
import json
import confs


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
		code = request.GET.get('code', False)

		if not request:
			return False

		if vendor and vendor == 'insta':
			if not code:
				return ResponseManager.redirect(insta.INSTA_URL)
			else:
				_api = _im(request)
				user_info = _api.authenticate_user(code)
				print user_info
				if user_info:
					fetch_status = DBManager.check_account(username=user_info.get('username'))
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

						return ResponseManager.simple_response({'login_status': True, 'account_status': account_status})
					else:
						if DBManager.create_account(user_info, request = request):
							#TODO: add session.cookies here
							return ResponseManager.simple_response({'login_status': True, 'account_status': 'new_account'})
						else:
							return ResponseManager.simple_response({'login_status': False, 'account_status': 'creation_failed'})
				return ResponseManager.simple_response({'login_status': False, 'account_status': 'permission_failed'})

	@classmethod
	def init_account(self):
		"""
		This function will create a new account
		"""
		pass

	@classmethod
	def check_token_validity(self, token, vendor=None):
		"""
		Check if Token is still valid or not, if not update
		user model with token exception
		"""
		pass


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
		account = models.Account.objects.all()
		if account and len(account) > 0:
			if account[0].username == username:
				return account[0].fetch_status
		return False


	@classmethod
	def create_account(self, user_info, request = None,  **kwargs):
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
											slogan = user_info.get('slogan', ''),
											profile_picture = user_info.get('profile_picture'),
											first_name = user_info.get('full_name'),
											insta_id = user_info.get('id'),
											insta_token = request.session['access_token'],
											fetch_status = 1)
			if account:
				return True
		return False


	@classmethod
	def last_id(self):
		latest = models.Post.objects.latest('id')
		return latest and latest.media_id


	@classmethod
	def delete_account(self):
		"""
		This function will delete account and all posts
		"""
		pass

	@classmethod
	def create_posts(self, posts, account_reference):
		"""
		This function will create new posts in database
		its going to be bulk function
		"""


		db_posts = []
		for post in posts:
			single_post = models.Post(
								media_id = post.get('media_id'),
								title = post.get('description'),
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
	def get_posts(self, last_id=None):
		"""
		This function will fetch posts from database
		"""
		final_result = False
		posts = models.Post.objects.all()
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
	def get_posts(self, last_id=None):
		"""
		This function will fetch posts from cache
		"""
		pass

	@classmethod
	def get_db(self, last_id=None):
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
	def fetch_posts(self, vendor='insta', username = None, last_id=None):
		"""
		This function will fetch posts from vendors
		"""
		token = None
		client_secret = confs.CLIENT_SECRET
		count_limit = 20
		last_media_id = last_id
		loop_flag = True
		posts = []

		print 'here'
		if vendor and vendor == 'insta' and username:
			account = models.Account.objects.filter(username=username)
			print 'dfd', len(account)
			if account and len(account) > 0:
				token = account[0].insta_token
				print 'insta_token', token
				if token:
					api = InstagramAPI(access_token=token, client_secret=client_secret)
					while loop_flag:
						recent_media, next = api.user_recent_media(
																	count = count_limit,
																	max_id = last_media_id)
						for media in recent_media:
							last_media_id = media.id
							posts.append({ 	'media_id': media.id,
										 	'description': self.verify_property(media, 'caption') or '',
										 	'date_published': self.verify_property(media, 'created_time'),
											'post_type': self.check_media_type(media, 'type'),
											'post_url': media.get_standard_resolution_url(),
											'post_tags': self.make_tags(media, 'tags'),
											'location': self.verify_property(media, 'location'),
											'location_name': self.verify_property(media, 'location.name'),
											'account': None
										})
						loop_flag = len(recent_media) > 0

					return posts

		return False

	@classmethod
	def verify_property(self, obj, prop):
		if hasattr(obj, prop):
			return getattr(obj, prop)
		return None

	@classmethod
	def check_media_type(self, obj, prop):
		media_type = self.verify_property(obj, prop)
		if media_type:
			if media_type == 'image':
				return 1
			elif media_type == 'video':
				return 2
			else:
				return 3


	@classmethod
	def make_tags(self, media, tags):
		tags = self.verify_property(media, tags)
		if tags:
			new_tags = []
			for tag in tags:
				new_tags.append(tag.name)
			return json.dumps(new_tags)
		return False


# def initiate_setup(self):
# 		"""
# 		grabs the data and updates the database
# 		"""
# 		user_obj = {}
# 		fresh_media = []
# 		count_limit = 20
# 		last_media_id = None
# 		loop_flag = True
# 		access_token = self.request.session['access_token']
# 		api = InstagramAPI(access_token=access_token, client_secret=self.CONFIG['client_secret'])

# 		while loop_flag:
# 			recent_media, next = api.user_recent_media(count=count_limit, max_id=last_media_id)
# 			for media in recent_media:
# 				last_media_id = media.id
# 				fresh_media.append({ 'media_id': media.id,
# 									 'description': self.verify_property(media, 'caption'),
# 									 'date_published': self.verify_property(media, 'created_time'),
# 									 'post_type': self.verify_property(media, 'type'),
# 									 'post_url': media.get_standard_resolution_url(),
# 									 'post_tags': self.make_tags(media, 'tags'),
# 									 'location': self.verify_property(media, 'location'),
# 									 'location_name': self.verify_property(media, 'location.name'),
# 									})
# 			loop_flag = len(recent_media) > 0
# 		if len(fresh_media) > 0:
# 			print fresh_media
# 			return True #update data base here with user data and snaps
# 		return False

class Provider(object):

	@classmethod
	@response_wrapper
	def get_posts(self, last_id=None):
		"""
		get posts, if not, check account,
		"""
		posts = DBManager.get_posts(last_id = last_id)
		if posts:
			return self.make_posts(posts)
		else:
			accounts = models.Account.object.add()
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
	def make_posts(self, posts):
		posts_dict = self.make_dict(True, 'posts', 'fetch_completed')
		posts_container = []
		for post in posts:
			posts_container.append({ 'title': post.title
									})

		posts_dict['posts'] = posts_container
		return posts_dict

	@classmethod
	def fetch_update_posts(self, vendor='insta', username=None, last_id = None):
		#TODO: get last data id from database
		last_id = DBManager.last_id()
		last_id = last_id or None

		posts = FetchManager.fetch_posts(vendor=vendor, username=username, last_id = last_id)
		account = models.Account.objects.filter(username=username)
		if account and len(account) > 0 and DBManager.create_posts(posts, account[0]):
			return ResponseManager.simple_response({'status': 'success', 'fetch_status': 'complete'})
		return ResponseManager.simple_response({'status': 'failed', 'fetch_status': 'not_completed'})

	@classmethod
	def troll(self):
		return ResponseManager.simple_response({'hey': ';)'})





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











