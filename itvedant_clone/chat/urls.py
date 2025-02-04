from django.urls import path
from . import views

urlpatterns = [
    path('start-chat/', views.start_chat, name='start_chat'),
    path('chat-session/<int:session_id>/', views.chat_session, name='chat_session'),
    path('public-chat/', views.public_chat, name='public_chat'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),

]
