from django.contrib import admin
from .models import *
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'coordinator')  # Show these fields in the admin panel
    search_fields = ('title',)  # Enable searching by title
    list_filter = ('coordinator',)  # Add filtering by coordinator

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')  # Show these fields
    search_fields = ('title', 'course__title')  # Search by chapter title and course title
    list_filter = ('course',)  # Add filtering by course

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'completed')  # Show user progress
    list_filter = ('completed', 'user')  # Add filtering options



@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'created_at', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'posted_by')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'applied_at')
    list_filter = ('job', 'user')
