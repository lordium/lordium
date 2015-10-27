import models

class LoginManager(object):
	"""
	This manager is responsible for geting login signal from
	client, redirecting to external vendor, and fetching user
	access token, and managing it.
	"""

	@classmethod
	def check_account(self):
		"""
		This function will check if account exists or not
		"""
		pass

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
	def create_account(self):
		"""
		This function will create account and write it to
		database
		"""
		pass

	@classmethod
	def delete_account(self):
		"""
		This function will delete account and all posts
		"""
		pass

	@classmethod
	def create_posts(self):
		"""
		This function will create new posts in database
		"""
		pass

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


class Provider(object):

	@classmethod
	def get_posts(self, last_id=None):
		"""
		get posts, if not, check account,
		"""
		final_result = False
		posts = DBManager.get_posts()
		if posts:
			return self.make_posts(posts)
		else:
			accounts = models.Account.object.add()
			if accounts and len(accounts) > 0:
				if accounts[0].fetch_status == 1: #1 => NEW
					return self.make_dict(True, 'no_posts', 1)
				elif accounts[0].fetch_status == 2: #2 => Fetching
				 	return self.make_dict(True, 'no_posts', 2)
				elif accounts[0].fetch_status == 3: #3 => Fetch Completed
					return self.make_dict(True, 'no_posts', 3)
			else:
				return self.make_dict(False, 'no_posts', 0)
		return final_result

	@classmethod
	def make_dict(self, success=True, data_type=None, account_status=None):
		return {'success': success,
				'data_type': data_type,
				'account_status': account_status}

	@classmethod
	def make_posts(self, posts):
		posts_dict = self.make_dict(True, 'posts', 3)
		posts_container = []
		for post in posts:
			posts_container.append({ 'title': post.title
									})

		posts_dict['posts'] = posts_container
		return posts_dict








