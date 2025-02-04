from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/mark-done/<int:chapter_id>/', views.mark_chapter_complete, name='mark_chapter_complete'),
    path('create-chapter/', views.create_chapter, name='create_chapter'),
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("staff/create-job/", views.create_job, name="create_job"),    
    
]
