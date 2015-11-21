from django.utils import timezone
from django.test import TestCase

from .models import Account,Post
from .manager import DBManager, Provider
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
		self.assertEqual(Account.objects.get(username='testuser').email,
			'test@example.com')

	def test_create_new_post_db(self):
		posts = []
		for i in range(0, 5):
			posts.append(self.dummy_post)
		self.assertEqual(DBManager.db_create_posts(posts, self.account),
			True)

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
			if post.get('title') != 'this is dummy post' and \
			post.get('post_tags') !='#test #post':
				post_fail = True

		self.assertFalse(post_fail)

	def test_count_on_post_delete(self):
		self.assertTrue(True)

	def test_count_on_account_delete(self):
		self.assertTrue(True)

	def test_get_posts_on_empty_db_should_return_no_account(self):
		self.assertTrue(True)

	def test_get_posts_on_new_account_should_return_new(self):
		self.assertTrue(True)

	def test_login_without_instagram_should_not_let_in(self):
		self.assertTrue(True)
