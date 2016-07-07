from django.contrib import admin

from .models import Thread, Comment
# Register your models here.

admin.site.register(Thread)
admin.site.register(Comment)