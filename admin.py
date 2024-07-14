from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(signupdetail)
admin.site.register(userlogin)
admin.site.register(addbook)
admin.site.register(view)
admin.site.register(IssueBooks)
admin.site.register(Updatebook)
admin.site.register(returnbooks)
admin.site.register(FacultyIssueBooks)
admin.site.register(Facultyreturnbooks)

# class viewbook(admin.ModelAdmin):
#   list_display = ("book_id", "book_name",)

# admin.site.register(view, viewbook)