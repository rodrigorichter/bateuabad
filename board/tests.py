from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from django.test import TestCase, Client
from .models import Thread, Comment
from django.core.urlresolvers import reverse
from .forms import CommentForm, ThreadForm

class ThreadMethodTests(TestCase):
	def test_was_published_recently_with_Thread(self):
		"""
		was_published_recently() should return True for Threads published recently
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_Thread = Thread(pubDate=time)
		self.assertEqual(recent_Thread.was_published_recently(), True)

def create_Thread(text, days):
	"""
	Creates a Thread with the given `text` and published the
	given number of `days` offset to now (negative for Threads published
	in the past, positive for Threads that have yet to be published).
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Thread.objects.create(text=text, pubDate=time)

def create_Comment(text, days, thread):
	"""
	Creates a Comment with the given `text` and published the
	given number of `days` offset to now (negative for Comments published
	in the past, positive for Comments that have yet to be published).
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Comment.objects.create(text=text, pubDate=time, thread=thread)


class ThreadViewTests(TestCase):
	def test_index_view_with_no_Threads(self):
		"""
		If no Threads exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('board:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No threads are available.")
		self.assertQuerysetEqual(response.context['latest_thread_list'], [])

	def test_index_view_with_a_past_Thread(self):
		"""
		Threads with a pubDate in the past should be displayed on the
		index page.
		"""
		create_Thread(text="Past Thread.", days=-30)
		response = self.client.get(reverse('board:index'))
		self.assertQuerysetEqual(
			response.context['latest_thread_list'],
			['<Thread: Past Thread.>']
		)

	def test_index_view_with_two_past_Threads(self):
		"""
		The Threads index page may display multiple Threads.
		"""
		create_Thread(text="Past Thread 1.", days=-30)
		create_Thread(text="Past Thread 2.", days=-5)
		response = self.client.get(reverse('board:index'))
		self.assertQuerysetEqual(
			response.context['latest_thread_list'],
			['<Thread: Past Thread 2.>', '<Thread: Past Thread 1.>']
		)

class ThreadIndexDetailTests(TestCase):

	def test_detail_view_with_a_past_Thread(self):
		"""
		The detail view of a Thread with a pubDate in the past should
		display the Thread's text.
		"""
		past_Thread = create_Thread(text='Past Thread.', days=-5)
		url = reverse('board:detail', args=(past_Thread.id,))
		response = self.client.get(url)
		self.assertContains(response, past_Thread.text)

	def test_detail_view_with_no_comments(self):
		"""
		The detail view of a Thread with a pubDate in the past should
		display the error message when there are no comments
		"""
		past_Thread = create_Thread(text='Past Thread.', days=-5)
		url = reverse('board:detail', args=(past_Thread.id,))
		response = self.client.get(url)
		self.assertContains(response, "Nenhum comentario ainda :(")

	def test_detail_view_with_one_comments(self):
		"""
		The detail view of a Thread with one comment should display it
		"""
		past_Thread = create_Thread(text='Past Thread.', days=-5)
		past_Comment = create_Comment(text='Past Comment.', days=-5, thread=past_Thread)
		url = reverse('board:detail', args=(past_Thread.id,))
		response = self.client.get(url)
		self.assertContains(response, past_Comment.text)

	def test_detail_view_with_multiple_comments(self):
		"""
		The detail view of a Thread with one comment should display it
		"""
		past_Thread = create_Thread(text='Past Thread.', days=-5)
		past_Comment = create_Comment(text='Past Comment.', days=-5, thread=past_Thread)
		past_Comment2 = create_Comment(text='Past Comment2.', days=-5, thread=past_Thread)
		past_Comment3 = create_Comment(text='Past Comment3.', days=-5, thread=past_Thread)
		url = reverse('board:detail', args=(past_Thread.id,))
		response = self.client.get(url)
		self.assertContains(response, past_Comment.text)
		self.assertContains(response, past_Comment2.text)
		self.assertContains(response, past_Comment3.text)

class ThreadAddthreadTests(TestCase):
	def test_addthread_with_empty_text(self):
		"""
		The request should return to the same page and include an error when 
		text field is empty
		"""
		c = Client()
		formData = {'title': 'eae', 'text': '', 'pubDate': timezone.now()}
		response = c.post('/board/addthread/', formData, follow=True)
		self.assertContains(response, "This field is required.")

	def test_addthread_with_text(self):
		"""
		The request should create the thread and go to its detail view when the
		text field is not empty
		"""
		c = Client()
		formData = {'title': 'eae', 'text': 'this is a text', 'pubDate': timezone.now()}
		response = c.post('/board/addthread/', formData, follow=True)
		self.assertContains(response, "this is a text")

	def test_addthread_with_empy_title(self):
		"""
		The request should create the thread and go to its detail view when the
		title field is empty
		"""
		c = Client()
		formData = {'title': '', 'text': 'this is a text', 'pubDate': timezone.now()}
		response = c.post('/board/addthread/', formData, follow=True)
		self.assertContains(response, "this is a text")

	class CommentAddCommentTests(TestCase):
		def test_addcomment_with_empy_text(self):
			"""
			The request should return to the same page and include an error when 
			text field is empty
			"""
			dummyThread = create_Thread(text='thread text.', days=-5)
			c = Client()
			formData = {'author': 'eae', 'text': '', 'pubDate': timezone.now()}
			response = c.post('/board/addthread/1/addcomment/', formData, follow=True)
			self.assertContains(response, "This field is required.")

		def test_addcomment_with_text(self):
			"""
			The request should create the comment and go to its thread detail view when the
			text field is not empty
			"""
			dummyThread = create_Thread(text='this is a thread text', days=-5)
			c = Client()
			formData = {'author': 'eae', 'text': 'this is a comment text', 'pubDate': timezone.now()}
			response = c.post('/board/addthread/1/addcomment/', formData, follow=True)
			self.assertContains(response, "this is a thread text")
			self.assertContains(response, "this is a comment text")

		def test_addcomment_with_empty_author(self):
			"""
			The request should create the comment and go to its thread detail view when the
			author field is empty
			"""
			dummyThread = create_Thread(text='this is a thread text', days=-5)
			c = Client()
			formData = {'author': '', 'text': 'this is a comment text', 'pubDate': timezone.now()}
			response = c.post('/board/addthread/1/addcomment/', formData, follow=True)
			self.assertContains(response, "this is a thread text")
			self.assertContains(response, "this is a comment text")