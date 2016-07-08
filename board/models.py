from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone

class Thread(models.Model):
	title = models.CharField(max_length=80, blank=True, default='')
	text = models.TextField(max_length=2000)
	pubDate = models.DateTimeField('date published')
	latestCommentDate = models.DateTimeField('date published')

	def __str__(self):
		return self.text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pubDate <= now

	def update_last_comment_date(self):
		try:
			latestComment = self.comment_set.order_by('-pubDate')[0]
			self.latestCommentDate = latestComment.pubDate
			self.save()
		except IndexError:
			self.latestCommentDate = self.pubDate
			self.save()



class Comment(models.Model):
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	author = models.CharField(max_length=25, blank=True, default='')
	text = models.TextField(max_length=2000)
	pubDate = models.DateTimeField('date published')

	def __str__(self):
		return self.text

	def save(self, **kwargs):
		super(Comment, self).save(**kwargs)
		self.thread.update_last_comment_date()

	def delete(self):
		super(Comment, self).delete()
		self.thread.update_last_comment_date()