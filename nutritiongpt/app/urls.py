from django.urls import path
from . import views


urlpatterns = [
   path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
   path('logout/', views.logout, name='logout'),
   path('login/', views.login, name='login'),
   path('register/', views.register, name='register'),
   path('', views.index, name='index'),
   path('edit_profile/', views.edit_profile, name='edit_profile')
]
