from django.contrib import admin
from bookclub.models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Recommendation)
