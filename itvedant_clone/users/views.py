from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')  # ✅ Redirect to the correct dashboard
    return redirect('login')  # ✅ Redirect to login if not logged in


# Redirect users after login
@login_required
def dashboard_redirect(request):
    if request.user.is_staff:  # Staff user
        return redirect('staff_dashboard')
    else:  # Regular user
        return redirect('user_dashboard')

from courses.models import *
from django.db.models import Count, Q

@login_required
def user_dashboard(request):
    courses = Course.objects.all()
    
    # Progress calculation
    progress_data = {}
    for course in courses:
        total_chapters = course.chapters.count()  # Total chapters in the course
        completed_chapters = UserProgress.objects.filter(
            user=request.user, chapter__course=course, completed=True
        ).count()

        # Calculate progress percentage
        progress_data[course.id] = (completed_chapters / total_chapters * 100) if total_chapters else 0
    
    return render(request, 'users/user_dashboard.html', {
        'courses': courses,
        'progress_data': progress_data,
    })



@login_required
@user_passes_test(lambda user: user.is_staff)  # Only staff can access
def staff_dashboard(request):
    return render(request, 'users/staff_dashboard.html')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect('/users/dashboard/')  # Redirect to dashboard
    else:
        form = UserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')  # Redirect to login after logout

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileUpdateForm

@login_required
def profile(request):
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")  # Redirect to refresh page with updated info

        # Handle password change if the form is submitted
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Prevent logout after password change
            messages.success(request, "Your password has been updated successfully!")
            return redirect("profile")

    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, "users/profile.html", {
        "profile_form": profile_form,
        "password_form": password_form,
    })

from django.utils import timezone
from datetime import timedelta
from django.contrib.sessions.models import Session
from django.http import JsonResponse


def user_stats(request):
    # Get the total number of users
    total_users = User.objects.count()

    # Get the online users (users who have logged in within the last 5 minutes)
    time_threshold = timezone.now() - timedelta(minutes=5)
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Extract valid user IDs from active sessions
    user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions if session.get_decoded().get('_auth_user_id')]

    online_users = User.objects.filter(id__in=user_ids).count()

    return JsonResponse({"total_users": total_users, "online_users": online_users})


# leaderboard

def leaderboard(request):
    leaderboard_data = (
        User.objects
        .filter(is_staff=False, is_superuser=False)  # Exclude staff & admin
        .annotate(total_completed=Count('userprogress', filter=Q(userprogress__completed=True)))
        .order_by('-total_completed')
    )

    return render(request, 'users/leaderboard.html', {'leaderboard': leaderboard_data})

