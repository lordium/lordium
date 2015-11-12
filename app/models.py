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
	(4, _("Dirty"))
)



class Account(User):

	# username = models.CharField(max_length=140, unique=True) # check with instagram
	# email = models.EmailField(default=None, unique=True, null=True)

	insta_id = models.CharField(max_length=140, unique=True, null=True)
	insta_token = models.TextField("Token", null=True)
	# first_name = models.CharField(max_length=40, null=True)
	# last_name = models.CharField(max_length=40, null=True)
	profile_picture = models.TextField(validators=[URLValidator()],null=True)
	slogan = models.CharField(max_length=140, null=True)
	# date_created = models.DateTimeField(auto_now_add=True)
	# date_update = models.DateTimeField(auto_now=True)
	fetch_status = models.IntegerField(choices=FETCH_STATUS, default=0,
		help_text=_('Shows account status for fetching posts'))
	read_only = models.BooleanField(default=False, verbose_name="Read only",
		help_text=_('Allows read only on all resources'))
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
			   fetch_status = None
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
						fetch_status = fetch_status)
		account.set_password(username)
		account.backend='django.contrib.auth.backends.ModelBackend'

		if len(Account.objects.all()) == 0:
			account.is_superuser = True
			account.is_staff = True

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



