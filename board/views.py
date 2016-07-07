from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .forms import CommentForm, ThreadForm
from .models import Comment, Thread


class IndexView(generic.ListView):
	template_name = 'board/index.html'
	context_object_name = 'latest_thread_list'

	def get_queryset(self):
		"""
		Return the last five published threads (not including those set to be
		published in the future).
		"""
		return Thread.objects.filter(
			pubDate__lte=timezone.now()
		).order_by('-pubDate')


class DetailView(generic.DetailView):
	model = Thread
	template_name = 'board/detail.html'

def addcomment(request, pk):
	thread = get_object_or_404(Thread, pk=pk)

	if request.method == "POST":
		form = CommentForm(request.POST)

		if form.is_valid():
			comment = form.save(commit=False)
			comment.thread = thread
			comment.pubDate = timezone.now()
			comment.save()

			return redirect('board:detail', pk=thread.pk)
	else:
		form = CommentForm()

	return render(request, 'board/addcomment.html', {'form': form, 'pk': pk})

def addthread(request):

	if request.method == "POST":
		form = ThreadForm(request.POST)

		if form.is_valid():
			thread = form.save(commit=False)
			thread.pubDate = timezone.now()
			thread.save()

			return redirect('board:detail', pk=thread.pk)
	else:
		form = ThreadForm()

	return render(request, 'board/addthread.html', {'form': form})