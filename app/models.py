from django.db import models
from django.contrib.auth.models import AbstractBaseUser,User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import URLValidator
from django.contrib.auth.models import Permission
from django.core import validators
# Create your models here.

MEDIA_CHOICES = (
    (1, _("Image")),
    (2, _("Video"))
)

FETCH_STATUS = (
	(0, _("Not Registered")),
	(1, _("New")),
	(2, _("Fetching")),
	(3, _("Fetch Completed")),
	(4, _("Need Fetch"))
)

class GlobalConf(models.Model):
	"""
	Singleton global app Configuration
	"""

	instagram_app_id = models.CharField(max_length=140,verbose_name="App id",
		help_text=_('Instagram app id (Client id)'))
	instagram_app_secret = models.CharField(max_length=140,verbose_name="App Secret",
		help_text=_('Instagram app secret (Client Secret)'))
	google_analytics = models.TextField(verbose_name="Google Analytics",
		help_text=_('Google analytics script'), null=True)
	total_posts = models.IntegerField(verbose_name="Total Posts", default=0)
	total_accounts = models.IntegerField(verbose_name="Total Accounts", default=0)
	last_fetched = models.DateTimeField(verbose_name="Last Fetched", null=True)
	website_url = models.CharField(max_length=140, verbose_name="Website URL", null=True)
	insta_connected = models.BooleanField(verbose_name="App connected", default=False)
	description = models.TextField(verbose_name="Brand description",
		help_text=_('Please describe your brand, this will be used by \
			search engines'),
		 null=True)
	title = models.CharField(max_length=140, verbose_name="Brand slogan",
		help_text=_('Please write your brand slogan'),
		 null=True)

	class Meta:
		verbose_name = "Setting"

	def delete(self, *args, **kwargs):
		pass

	def save(self, *args, **kwargs):
		self.pk = 1
		super(GlobalConf, self).save(*args, **kwargs)

	@classmethod
	def get_config(self, instagram_app_id=None, instagram_app_secret=None,
		website_url=None):
		try:
			config = self.objects.get()
		except:
			pass
		if not config:
			config = self(instagram_app_id=instagram_app_id,
			instagram_app_secret=instagram_app_secret, website_url=website_url)
			config.save()
		elif config.insta_connected == False:
			config.instagram_app_id = instagram_app_id
			config.instagram_app_secret = instagram_app_secret
			config.website_url = website_url
			config.save()
		return config


class Account(User):

	# username = models.CharField(max_length=140, unique=True) # check with instagram
	# email = models.EmailField(default=None, unique=True, null=True)

	insta_id = models.CharField(max_length=140, unique=True, null=True)
	insta_token = models.TextField("Token", null=True)
	profile_picture = models.TextField(validators=[URLValidator()],null=True)
	slogan = models.CharField(max_length=140, null=True)
	fetch_status = models.IntegerField(choices=FETCH_STATUS, default=0,
		help_text=_('Shows account status for fetching posts'))
	read_only = models.BooleanField(default=False, verbose_name="Read only",
		help_text=_('Allows read only on all resources'))
	is_brand = models.BooleanField(default=False, verbose_name="Is Brand",
		help_text=_('This account will be displayed on front page'))
	# backend = ""

	# USERNAME_FIELD =  ['username']

	# def __str__(self):
	# 	return self.username

	# def __unicode__(self):
	# 	return self.username

	class Meta:
		verbose_name = "Account"
		# labels = {
		# 	'username': _('Writer'),
		# 	}
		# help_texts = {
		# 	'is_active': _('Some useful help text.'),
		# 	}

	def __init__(self, *args, **kwargs):
		super(Account, self).__init__(*args, **kwargs)
		# self.fields['username'].help_text = '<br/>Hold down "Control" to select more.'
		# Making name required
		# self.fields['last_name'].required = True
		# self.fields['email'].required = True

		# self.fields['bio'].required = True
		# self.fields['profession'].required = True

	@classmethod
	def create(self,
			   username=None,
			   email = None,
			   insta_token = None,
			   insta_id = None,
			   first_name = None,
			   last_name = None,
			   profile_picture = None,
			   slogan = None,
			   fetch_status = None,
			   is_brand=False
			   ):

		account = Account(
						username = username,
						email = email,
						insta_token = insta_token,
						insta_id = insta_id,
						first_name = first_name,
						last_name = last_name,
						profile_picture = profile_picture,
						slogan = slogan,
						fetch_status = fetch_status,
						is_brand=is_brand)
		account.set_password(username)
		account.backend='django.contrib.auth.backends.ModelBackend'

		if len(Account.objects.all()) == 0:
			account.is_superuser = True
			account.is_staff = True

			conf = GlobalConf.objects.get()
			conf.total_accounts += 1
			conf.save()

		account.save()
		return account

	@classmethod
	def partial_create(self,
			   username=None,
			   email = None,
			   insta_token = None,
			   insta_id = None,
			   first_name = None,
			   last_name = None,
			   profile_picture = None,
			   slogan = None,
			   fetch_status = None
			   ):

		account = Account.objects.get(username=username)
		if account:
			account.__dict__.update({
					'username':username,
					'email':email,
					'insta_token':insta_token,
					'insta_id':insta_id,
					'first_name':first_name,
					'last_name':last_name,
					'profile_picture':profile_picture,
					'slogan':slogan,
					'fetch_status':fetch_status
				})
			account.set_password(username)
			account.backend='django.contrib.auth.backends.ModelBackend'
			account.is_superuser = True
			account.is_staff = True
			account.save()

			conf = GlobalConf.objects.get()
			conf.total_accounts += 1
			conf.save()

			return account
		return False

	@classmethod
	def authenticate(self, username=None, password=None):
		try:
		    account = Account.objects.get(username=username)
		    if account.check_password(password):
		        return account
		except Account.DoesNotExist:
		    return None

	def account_image(self):
		profile_url = self.profile_picture or '/static/images/insta.png'
		return '<img src="%s" class=""/>' % profile_url
	account_image.allow_tags = True


	def delete(self):
		super(Account, self).delete()
		conf = GlobalConf.objects.get()
		conf.total_accounts -= 1
		conf.save()


class Post(models.Model):
	media_id = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200, null=True)
	date_published = models.DateTimeField("Date Published")
	post_type = models.IntegerField(choices=MEDIA_CHOICES, default=1)
	post_url = models.TextField(validators=[URLValidator()],null=True)
	description = models.TextField("Description",null=True)
	post_tags = models.TextField("Tags",null=True)
	location = models.TextField("Location Coordinates",null=True)
	location_name = models.TextField("Location Name",null=True)
	account = models.ForeignKey(Account, null=True)

	def super_post_url(self):
		if self.post_type == 1:
			return '<img src="%s" class=""/>' % self.post_url
		else:
			return '<video class="" controls width="100%%" height="100%%"><source src="%s" type="video/mp4"/></video>' % self.post_url

	super_post_url.allow_tags = True



	@classmethod
	def post_bulk_create(self, posts):
		Post.objects.bulk_create(posts)
		total_posts = len(Post.objects.all())
		try:
			config = GlobalConf.objects.get()
			config.total_posts = total_posts
			config.save()
		except:
			pass
		return True

	@classmethod
	def filter_detail(description):
		"""
		Categorize title, description, and remove tags
		"""
		description = description
		title = "This is title"
		return title, description

	@classmethod
	def filter_tags(tags):
		"""
		Gets a list of tag objects and returns json object
		"""
		json_tag = []
		for tag in tags:
			json_tag.append(tag.name)
		return json.dumps(json_tag)

	@classmethod
	def verify_fields():
		pass

	def delete(self):
		super(Post, self).delete()
		conf = GlobalConf.objects.get()
		conf.total_posts -= 1
		conf.save()



