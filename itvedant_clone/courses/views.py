from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Course, Chapter, UserProgress

# Check if user is staff
def is_staff(user):
    return user.is_staff

# Create course (restricted to staff)
@login_required
@user_passes_test(is_staff)
def create_course(request):
    if request.method == 'POST':
        # Implement course creation logic here
        pass
    return render(request, 'courses/create_course.html')

# List of courses (restricted to logged-in users)
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# Course detail view with AJAX-based question checking
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapters = course.chapters.all()

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        chapter_id = request.POST.get('chapter_id')
        user_answer = request.POST.get('user_answer')

        chapter = get_object_or_404(Chapter, id=chapter_id)
        correct = user_answer.strip().lower() == chapter.answer.strip().lower()

        return JsonResponse({'correct': correct})

    return render(request, 'courses/course_detail.html', {'course': course, 'chapters': chapters})

@login_required
def mark_chapter_complete(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    progress, created = UserProgress.objects.get_or_create(user=request.user, chapter=chapter)
    progress.completed = True
    progress.save()
    messages.success(request, "Chapter marked as complete!")
    return redirect("course_detail", course_id=chapter.course.id)  # ✅ Fixed

from .forms import ChapterForm

@login_required
@user_passes_test(lambda user: user.is_staff)
def create_chapter(request):
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Chapter created successfully!")
            return redirect('staff_dashboard')  # Redirect to staff dashboard
    else:
        form = ChapterForm()

    return render(request, 'courses/create_chapter.html', {'form': form})

# Staff Dashboard - Create Jobs

from .models import JobListing, JobApplication

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        requirements = request.POST.get("requirements")

        if title and description and requirements:
            JobListing.objects.create(
                title=title, description=description, requirements=requirements, posted_by=request.user
            )
            messages.success(request, "Job posted successfully!")
            return redirect("staff_dashboard")

    return render(request, "courses/create_job.html")

# Job Listings for Users
@login_required
def job_list(request):
    jobs = JobListing.objects.all()
    applied_jobs = JobApplication.objects.filter(user=request.user).values_list("job_id", flat=True)
    return render(request, "courses/job_list.html", {"jobs": jobs, "applied_jobs": applied_jobs})

# Apply for a Job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if not JobApplication.objects.filter(user=request.user, job=job).exists():
        JobApplication.objects.create(user=request.user, job=job)
        messages.success(request, "You have successfully applied for this job!")
    else:
        messages.info(request, "You have already applied for this job.")
    
    return redirect("job_list")

