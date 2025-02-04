from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('user/', user_dashboard, name='user_dashboard'),
    path('staff/', staff_dashboard, name='staff_dashboard'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='custom_logout'),
    path("profile/", profile, name="profile"),
    path('user-stats/', user_stats, name='user_stats'),
    path('leaderboard/', leaderboard, name='leaderboard'),

]
