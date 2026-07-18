from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/reset/', views.chat_reset, name='chat_reset'),
]
