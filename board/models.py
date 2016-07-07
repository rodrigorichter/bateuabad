from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone

class Thread(models.Model):
	title = models.CharField(max_length=80, blank=True, default='')
	text = models.TextField(max_length=2000)
	pubDate = models.DateTimeField('date published')

	def __str__(self):
		return self.text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pubDate <= now


class Comment(models.Model):
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	author = models.CharField(max_length=25, blank=True, default='')
	text = models.TextField(max_length=2000)
	pubDate = models.DateTimeField('date published')

	def __str__(self):
		return self.text
