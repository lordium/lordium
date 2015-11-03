import requests
from django.conf import settings
from instagram.client import InstagramAPI
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect

class Darbaan(object):

	def __init__(self, request, vendor='insta', **kwargs):
		self.redirect_url = getattr(settings, 'REDIRECT_URI', None)
		self.success_url = '/'
		self.request = request


	def insta_login(self, code, **kwargs):
		if not code:
			return self.insta_redirect()

		config = getattr(settings, 'SOCIAL_AUTH', None)
		if config:
			config = config.get('insta', None)
			config['redirect_uri'] = self.redirect_url

		unauthenticated_insta = InstagramAPI(**config)
		access_token, user_info = unauthenticated_insta.exchange_code_for_access_token(code)
		self.request.session['access_token'] = access_token
		return user_info

	@classmethod
	def insta_redirect(self):
		redirect_url = getattr(settings, 'SOCIAL_HOOKS', None)
		redirect_url = redirect_url.get('insta', None)
		return HttpResponseRedirect(redirect_url.get('insta_url','/'))


	@classmethod
	def insta_fetch(self, token=None, count_limit = 20, last_id  = None):
		last_media_id = last_id
		loop_flag = True
		posts = []
		if token:
			client_secret = getattr(settings, 'SOCIAL_AUTH').get('insta').get('client_secret')
			api = InstagramAPI(access_token=token, client_secret=client_secret)
			while loop_flag:
				recent_media, next = api.user_recent_media(
															count = count_limit,
															max_id = last_media_id)
				for media in recent_media:
					print media
					last_media_id = media.id
					posts.append({ 	'media_id': media.id,
								 	'description': self.verify_property(media, 'caption') or '',
								 	'date_published': self.verify_property(media, 'created_time'),
									'post_type': self.insta_check_type(media, 'type'),
									'post_url': media.get_standard_resolution_url(),
									'post_tags': self.verify_property(media, 'tags'),
									'location': self.verify_property(media, 'location'),
									'location_name': self.verify_property(media, 'location') and
										self.verify_property(media, 'location').name,
									'account': None
								})
				loop_flag = len(recent_media) > 0
		return posts


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


	# @classmethod
	# def fm_make_tags(self, media, tags):
	# 	tags = self.verify_property(media, tags)
	# 	if tags:
	# 		new_tags = []
	# 		for tag in tags:
	# 			new_tags.append(tag.name)
	# 		return json.dumps(new_tags)
	# 	return False