
from instagram.client import InstagramAPI
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from models import Account
import requests
import json
import confs

## get secret and data from wherever you want.
INSTA_URL = confs.INSTA_URL
REDIRECT_URI = confs.REDIRECT_URI
INSTA_ACCESS_URI = confs.INSTA_ACCESS_URI
CLIENT_ID = confs.CLIENT_ID
CLIENT_SECRET = confs.CLIENT_SECRET

class InstaMine(InstagramAPI):
	"""
	Wrap the InstagramAPI and make something out of it
	"""
	authenticated_api = None #TODO: check if this not present then make a call
	CONFIG = {
	    'client_id': CLIENT_ID,
	    'client_secret': CLIENT_SECRET,
	    'redirect_uri': REDIRECT_URI
		 }
	user_info = None
	request = None
	def __init__(self, request, **kwargs):
		self.request = request
		kwargs.update(self.CONFIG)
		super(InstaMine, self).__init__(**kwargs)

	def authenticate_user(self, code):
		"""
		Authenticate user and get the access token
		"""
		access_token, user_info = self.exchange_code_for_access_token(code)
		self.authenticated_api = InstagramAPI(access_token=access_token,
											  client_secret=self.CONFIG['client_secret'])
		self.user_info = user_info
		self.request.session['access_token'] = access_token
		return True

	def verify_property(self, obj, prop):
		if hasattr(obj, prop):
			return getattr(obj, prop)
		return None

	def make_tags(self, media, tags):
		tags = self.verify_property(media, tags)
		if tags:
			new_tags = []
			for tag in tags:
				new_tags.append(tag.name)
			return json.dumps(new_tags)
		return False

	def detect_user(self):
		"""
		Check if user exists already
		"""
		#check for user insta id
		if len(Account.objects.all()) < 1:
			return False
		for account in Account.objects.all():
			if account.username == self.user_info.username:
				return True #will show admin page
			else:
				#TODO: redirect to not allowed page
				pass

	def flow_manager(self):
		"""
		Check user, initiate or let user login
		"""

		user_status = self.detect_user()
		if user_status == False: #there is no user
			#initiate the setup
			self.create_user() #TODO: get user token here

			dummy = {'login': True, 'posts_status': 'fetching'}
			return json.dumps(dummy)
			# 1 create user success
			# 2 return response to user
			# 3 somehow initiage data gathering
			#TODO: return json with JSON.stringify({'login': true, 'posts_status': 'fetching'});
			return HttpResponseRedirect('/process_setup')

			# enable setup mode in responose
			# use ajax and angular view OK?
			return #Some json response

		if user_status == True:
			#let user login, he is already there
			return #only enable edit menus

	def create_user(self):
		"""
		Creates user on first login
		"""

		pass

	def initiate_setup(self):
		"""
		grabs the data and updates the database
		"""
		user_obj = {}
		fresh_media = []
		count_limit = 20
		last_media_id = None
		loop_flag = True
		access_token = self.request.session['access_token']
		api = InstagramAPI(access_token=access_token, client_secret=self.CONFIG['client_secret'])

		while loop_flag:
			recent_media, next = api.user_recent_media(count=count_limit, max_id=last_media_id)
			for media in recent_media:
				last_media_id = media.id
				fresh_media.append({ 'media_id': media.id,
									 'description': self.verify_property(media, 'caption'),
									 'date_published': self.verify_property(media, 'created_time'),
									 'post_type': self.verify_property(media, 'type'),
									 'post_url': media.get_standard_resolution_url(),
									 'post_tags': self.make_tags(media, 'tags'),
									 'location': self.verify_property(media, 'location'),
									 'location_name': self.verify_property(media, 'location.name'),
									})
			loop_flag = len(recent_media) > 0
		if len(fresh_media) > 0:
			print fresh_media
			return True #update data base here with user data and snaps
		return False

	def create_account(self):
		"""
		Update database and initiate account for user
		"""
		pass

	def update_account(self):
		"""
		Update user account
		"""
		pass

	def get_snaps(self):
		"""
		Get user images and make feed
		"""
		access_token = self.request.session['access_token']
		api = InstagramAPI(access_token=access_token, client_secret=self.CONFIG['client_secret'])
		max_id = '676084064456413232_1141033715' #'678239748572712988_1141033715' #'719640177034269005_1141033715' #'760556627710054786_1141033715' #'1045397096325845271_1141033715' #'1067358253143953511_1141033715'
		recent_media, next = api.user_recent_media(count=60, max_id=max_id)

		print len(recent_media)
		print next
		print next and next.split('max_id=') #IT works
		result = ""
		for media in recent_media:
			print media.type
			print media.id
			result+= '<img src="%s"/>'%media.get_standard_resolution_url()
			# result+='<h1>%s</h1>'%media.location and media.location.name or ''
			result+='<h1>%s</h1>'%media.created_time
			result+='<h1>%s</h1>'%media.caption
			tg = ''
			for tag in media.tags:
				print tag.name
			result+='<h1>%s</h1>'%tg
		return result

	def db_check_user(self):
		pass

	def db_fetch_status(self):
		pass

	def create_snaps(self):
		"""
		Create snaps for linked account
		"""
		pass


def get_user_obj(user_obj):
	return {
				'username': user_obj.get('username'),
				'insta_id': user_obj.get('id'),
				'full_name': user.get('full_name'),
				'slogan': user.get('bio'),
				'website': user.get('website'),
				'profile_picture': user.get('profile_picture')
			}

	#Get user data here
		#{u'username': u'arslanrafique', u'bio': u'Engineer, <3 Stockholm!', u'website': u'', u'profile_picture': u'https://scontent.cdninstagram.com/hphotos-xpf1/t51.2885-19/924761_778256512251267_1485306869_a.jpg', u'full_name': u'Arslan Rafique', u'id': u'1141033715'}





