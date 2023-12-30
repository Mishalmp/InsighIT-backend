from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Topics)
admin.site.register(Blogs)
admin.site.register(Report_blog)
admin.site.register(Like)
admin.site.register(SavedBlogs)
admin.site.register(Community)