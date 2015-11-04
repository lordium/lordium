from django.utils import timezone
from django.test import TestCase

from app.models import Account,Post
from app.manager import DBManager, Provider
from datetime import datetime
from django.db import IntegrityError, transaction
import json
import re


class MainTest(TestCase):

	def setUp(self):
		Account.objects.create(
			username = 'testuser',
			email = 'test@example.com',
			insta_token = '234234234234',
			insta_id = '234234234',
			first_name = 'Test',
			last_name = 'User',
			profile_picture = 'http://localhost:8080/pic.png',
			slogan = 'Test Guy',
			fetch_status = 0)

		self.account = Account.objects.get(username='testuser')
		self.dummy_post = {
			'media_id': '1212',
			'title': 'this is dummy post',
			'description': 'this is dummy post',
			'date_published': datetime.now(),
			'post_type': 1,
			'post_url': 'http://localhost:8000/post.png',
			'post_tags': "#test #post",
			'location': '12.123123, 21.21212',
			'location_name': 'Sweden',
			}

		self.dummy_post_wrong = {
			'media_id': '1212',
			'title': 'this is dummy post',
			'description': 'this is dummy post',
			'date_published': datetime.now(),
			'post_type': 1,
			'post_url': 'http://localhost:8000/post.png',
			'post_tags': "#test #post",
			'location': '12.123123, 21.21212',
			'location_name': 'Sweden',
			}

	def test_create_new_account(self):
		self.assertEqual(Account.objects.get(username='testuser').email, 'test@example.com')

	def test_create_new_post_db(self):
		# DBManager.db_create_posts(self.dummy_post, self.account)
		posts = []
		for i in range(0, 5):
			posts.append(self.dummy_post)
		self.assertEqual(DBManager.db_create_posts(posts, self.account), True)

	def test_create_new_post_db_null_fail(self):
		posts = []
		null_fail = True
		for i in range(0, 5):
			posts.append(self.dummy_post_wrong)
			try:
				with transaction.atomic():
					DBManager.db_create_posts(posts, self.account)
			except IntegrityError:
				null_fail = False

		self.assertTrue(null_fail)

	def test_get_posts(self):
		posts = []
		for i in range(0, 5):
			posts.append(self.dummy_post)
		self.assertEqual(DBManager.db_create_posts(posts, self.account), True)

		posts_in_response = Provider.get_posts()
		posts_from_db = json.loads(posts_in_response.content)

		post_fail = False
		for post in posts_from_db.get('posts'):
			if post.get('title') != 'this is dummy post' and post.get('post_tags') !='#test #post':
				post_fail = True

		self.assertFalse(post_fail)


	def test_create_markup(self):
		import re
		data = "#bla #bla -- Great TEST -- test"
		result = ''
		# data = "-- Great TEST -- test"
		headMatch = re.match(r'(.*)--(.*)--(.*)', data)
		if headMatch:
			total_breaks = headMatch.groups()
			total_breaks_len = len(total_breaks)
			print headMatch.groups()
			# print headMatch.group(1)
			# print headMatch.group(2)
			# print headMatch.group(3)

			if total_breaks_len == 3:
				print total_breaks_len
				if headMatch.group(1) == '':
					print headMatch.group(2)
					result = re.sub('--.*?--', '', data)

			print result
			print data


	def test_comment(self):
		comment = 'Comment: arslanrafique said "#awesome #view #sunny #weather #plane #sun--best place--"'
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

		print "comment::"
		print title
		print description




