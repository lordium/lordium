import re
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
	def insta_fetch(self, token=None, count_limit = 20, last_id  = None , user_id=None):
		last_media_id = last_id
		loop_flag = True
		posts = []
		client_secret = getattr(settings, 'SOCIAL_AUTH').get('insta').get('client_secret')
		client_id = getattr(settings, 'SOCIAL_AUTH').get('insta').get('client_id')
		api = False
		if token:
			api = InstagramAPI(access_token=token, client_secret=client_secret)
			print 'api token'
		else:
			api = InstagramAPI(client_id=client_id, client_secret=client_secret)
			print 'api id'

		if api:
			print 'have api'
			while loop_flag:
				print 'while'
				print last_media_id
				recent_media, next = api.user_recent_media(	user_id=user_id,
															count = count_limit,
															max_id = last_media_id)
				print recent_media, next
				for media in recent_media:
					print media
					last_media_id = media.id
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
				loop_flag = len(recent_media) > 0
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
			for tag in tags:
				if tag != 'Tag:':
					final_tags+=',' + tag.split(',')[0]
			print 'final tags'
			print final_tags
			return final_tags

		return ''

	@classmethod
	def insta_get_title_description(self, media, comment):
		comment = self.verify_property(media, comment)
		if comment:
			comment = str(comment)
			data =  re.findall(r'(?=.*?\".*?\")(.*?)"(.*)"', comment)[0][1]
			title = ''
			description = data
			headMatch = re.match(r'(.*)--(.*)--(.*)', data)
			if headMatch:
				total_breaks = headMatch.groups()
				total_breaks_len = len(total_breaks)
				if total_breaks_len == 3:
					# if headMatch.group(1) == '':
					title = headMatch.group(2)
			return title, description
		else:
			return '', ''