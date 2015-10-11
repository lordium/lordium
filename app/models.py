from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import URLValidator
# Create your models here.

MEDIA_CHOICES = (
    (1, _("Image")),
    (2, _("Video"))
)
class Account(AbstractBaseUser):
	username = models.CharField(max_length=140, unique=True) # check with instagram
	email = models.EmailField(unique=True)
	insta_id = models.CharField(max_length=140, unique=True, null=True)
	insta_token = models.TextField("Token", null=True)
	first_name = models.CharField(max_length=40, null=True)
	last_name = models.CharField(max_length=40, null=True)
	slogan = models.CharField(max_length=140, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.username

	def __unicode__(self):
		return self.username

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



