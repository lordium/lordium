from __future__ import absolute_import

from celery import shared_task, task

from .manager import Provider as pd


@shared_task
def fetch_posts(*args, **kwargs):
	pd.fetch_update_posts()

@shared_task
def add(x, y):
	print "Here is periodic task"
	return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


