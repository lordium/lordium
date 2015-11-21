from django.test import TestCase
from .darbaan import Darbaan as dab

class DarbaanTest(TestCase):
	def test_title_separator_from_description(self):
		comment = 'Comment: arslanrafique said "#test-A beautiful sunny \
day-#awesome #view #sunny #weather #plane #sun-best place-"'
		# because media is an object
		class Object(object):
			pass
		media = Object()
		media.caption = comment
		title, description = dab.insta_get_title_description(media, 'caption')
		self.assertEqual(title, 'A beautiful sunny day')

	def test_title_separator_from_description_no_match(self):
		comment = 'Comment: arslanrafique said "#test A beautiful sunny day \
#awesome #view #sunny #weather #plane #sun best place"'
		# because media is an object
		class Object(object):
			pass
		media = Object()
		media.caption = comment
		title, description = dab.insta_get_title_description(media, 'caption')
		self.assertEqual(title, '')

	def test_title_separator_from_description_no_description(self):
		comment = ''
		# because media is an object
		class Object(object):
			pass
		media = Object()
		media.caption = comment
		title, description = dab.insta_get_title_description(media, 'caption')
		self.assertEqual(title, '')
