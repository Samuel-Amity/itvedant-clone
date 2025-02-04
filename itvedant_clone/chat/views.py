from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PublicChat
from django.contrib.auth.models import User
from django.db.models import Q


# Public Chat: Display open messages for all users
@login_required
def public_chat(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        PublicChat.objects.create(user=request.user, message=message_content)

    messages = PublicChat.objects.all().order_by('-timestamp')
    return render(request, 'chat/public_chat.html', {'messages': messages})

from .models import ChatSession, Message
import random

def start_chat(request):
    # When the user clicks the button to start the chat
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')  # User selects staff
        if staff_id:
            staff = get_object_or_404(User, id=staff_id)
        else:
            # Randomly select a staff member
            staff = random.choice(User.objects.filter(is_staff=True))
        
        # Create a chat session
        chat_session = ChatSession.objects.create(user=request.user, staff=staff)

        return redirect('chat_session', session_id=chat_session.id)  # Redirect to chat session page

    # Get all staff members
    staff_list = User.objects.filter(is_staff=True)
    return render(request, 'chat/start_chat.html', {'staff_list': staff_list})


def chat_session(request, session_id):
    chat_session = get_object_or_404(ChatSession, id=session_id)

    # Fetch all messages in the session
    messages = chat_session.messages.all().order_by('timestamp')

    # Handle new message submission
    if request.method == "POST":
        message_content = request.POST.get('message')
        if message_content:
            Message.objects.create(session=chat_session, sender=request.user, message=message_content)

    return render(request, 'chat/chat_session.html', {'chat_session': chat_session, 'messages': messages})


# chatbot

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        message = request.POST.get("message", "").strip()

        # Predefined responses
        responses = {
            "apply_jobs": "To apply for jobs, visit the 'Job Openings' section and click on 'Apply'.",
            "enroll_course": "To enroll in a course, go to the 'Courses' section and select your preferred course.",
            "progress_check": "You can check your progress in the 'Dashboard' under 'My Courses'."
        }

        response_text = responses.get(message, "I'm sorry, I didn't understand that.")
        return JsonResponse({"message": response_text})

    return JsonResponse({"message": "Invalid request."})
