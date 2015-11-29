import re
import requests
from django.conf import settings
from instagram.client import InstagramAPI
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect

INSTA_REDIRECT_URI = 'https://api.instagram.com/oauth/authorize/?client_id=%s\
&redirect_uri=%s&response_type=code'

class Darbaan(object):

	def __init__(self, request, vendor='insta', **kwargs):
		self.redirect_url = getattr(settings, 'REDIRECT_URI', None)
		self.success_url = '/'
		self.request = request

	def insta_login(self, code, **kwargs):
		if not code:
			return self.insta_redirect()

		config = {}
		config['client_id'] = kwargs.get('app_id')
		config['client_secret'] = kwargs.get('app_secret')
		config['redirect_uri'] = kwargs.get('website_url') + '/redirect_url/'
		unauthenticated_insta = InstagramAPI(**config)
		access_token, user_info = unauthenticated_insta.exchange_code_for_access_token(code)
		self.request.session['access_token'] = access_token
		return user_info

	@classmethod
	def insta_redirect(self, app_id=None, red_url=None):
		red_url = red_url + '/redirect_url/'
		# redirect_url = 'https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code'
		redirect_url = INSTA_REDIRECT_URI%(app_id, red_url)
		return HttpResponseRedirect(redirect_url)


	@classmethod
	def insta_fetch(self, app_id, app_secret, token=None, count_limit = 20, last_id  = None , user_id=None):
		last_media_id = last_id
		loop_flag = True
		posts = []
		# client_secret = getattr(settings, 'SOCIAL_AUTH').get('insta').get('client_secret')
		# client_id = getattr(settings, 'SOCIAL_AUTH').get('insta').get('client_id')
		client_secret = app_secret
		client_id = app_id
		api = False
		initiate = False
		api_args = {}
		if not last_media_id:
			api_args = {'user_id': user_id,
						'count': count_limit,
						'max_id': None
						}
			initiate = True
		else:
			api_args = {'user_id': user_id,
						'count': count_limit,
						'min_id': last_media_id
						}

		swap_args = None

		if token:
			api = InstagramAPI(access_token=token, client_secret=client_secret)
		else:
			api = InstagramAPI(client_id=client_id, client_secret=client_secret)

		if api:
			while loop_flag:
				recent_media = []
				swap_args = api_args
				try:
					recent_media, next = api.user_recent_media(**swap_args)
				except Exception, e:
					loop_flag = False
					recent_media = []
					print e
				for media in recent_media:
					if initiate:
						api_args['max_id'] = recent_media[-1]
					else:
						if not api_args['min_id'] == recent_media[-1]:
							api_args['min_id'] = recent_media[-1]
						else:
							recent_media = []
							loop_flag = False
							break
					title, description = self.insta_get_title_description(media, 'caption')
					posts.append({ 	'media_id': media.id,
									'title':title,
								 	'description': description,
								 	'date_published': self.verify_property(media, 'created_time'),
									'post_type': self.insta_check_type(media, 'type'),
									'post_url': media.get_standard_resolution_url(),
									'post_tags': self.insta_make_tags(media, 'tags'),
									'location': self.verify_property(media, 'location'),
									'location_name': self.verify_property(media, 'location') and
										self.verify_property(media, 'location').name,
									'account': None
								})

				print loop_flag
				if loop_flag:
					loop_flag = len(recent_media) > 0
				else:
					break

		return list(reversed(posts))


	@classmethod
	def verify_property(self, obj, prop):
		if hasattr(obj, prop):
			return getattr(obj, prop)
		return None

	@classmethod
	def insta_check_type(self, obj, prop):
		media_type = self.verify_property(obj, prop)
		if media_type:
			if media_type == 'video':
				return 2
		return 1


	@classmethod
	def insta_make_tags(self, media, tags):
		tags = self.verify_property(media, tags)
		if tags:
			tags = str(tags)
			tags = tags[1:-1].split()
			final_tags = ''
			sep = ','
			tags_len = len(tags)
			flag = True
			for tag in tags:
				if tag != 'Tag:':
					if flag:
						sep = ''
						flag = False
					else:
						sep = ','
					final_tags+=sep + tag.split(',')[0]
			return final_tags
		return ''

	@classmethod
	def insta_get_title_description(self, media, comment):
		comment = self.verify_property(media, comment)
		if comment:
			comment = str(comment)
			data =  re.findall(r'(?=.*?\".*?\")(.*?)"(.*)"', comment, re.DOTALL)[0][1]
			title = ''
			description = data
			headMatch = re.match(r'(.*?)-(.*?)-(.*?)', data) #? => non greedy
			if headMatch:
				total_breaks = headMatch.groups()
				total_breaks_len = len(total_breaks)
				if total_breaks_len == 3:
					# if headMatch.group(1) == '':
					title = headMatch.group(2)
				description = description.replace('-'+title+'-',' ')
			return title, description
		else:
			return '', ''