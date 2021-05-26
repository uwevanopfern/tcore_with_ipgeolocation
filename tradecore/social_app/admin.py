from django.contrib import admin
from .models import Location, Holiday, Post, Like

admin.site.register(Location)
admin.site.register(Holiday)
admin.site.register(Post)
admin.site.register(Like)
