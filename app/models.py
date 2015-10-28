from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import URLValidator
# Create your models here.

MEDIA_CHOICES = (
    ('image', _("Image")),
    ('video', _("Video"))
)

FETCH_STATUS = (
	(1, _("New")),
	(2, _("Fetching")),
	(3, _("Fetch Completed")),
)

class Account(AbstractBaseUser):
	username = models.CharField(max_length=140, unique=True) # check with instagram
	email = models.EmailField(default=None, unique=True, null=True)
	insta_id = models.CharField(max_length=140, unique=True, null=True)
	insta_token = models.TextField("Token", null=True)
	first_name = models.CharField(max_length=40, null=True)
	last_name = models.CharField(max_length=40, null=True)
	profile_picture = models.TextField(validators=[URLValidator()],null=True)
	slogan = models.CharField(max_length=140, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(auto_now=True)
	fetch_status = models.IntegerField(choices=FETCH_STATUS, default=1)

	def __str__(self):
		return self.username

	def __unicode__(self):
		return self.username

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

		account.save()
		return True


class Post(models.Model):
	media_id = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200)
	date_published = models.DateTimeField("Date Published")
	post_type = models.IntegerField(choices=MEDIA_CHOICES, default=1)
	post_url = models.TextField(validators=[URLValidator()],null=True)
	description = models.TextField("Description",null=True)
	post_tags = models.TextField("Tags",null=True)
	location = models.TextField("Location Coordinates",null=True)
	location_name = models.TextField("Location Name",null=True)
	account = models.ForeignKey(Account, null=True)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

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



