from django.urls import path
from . import views


urlpatterns = [
   path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
   path('logout/', views.logout, name='logout'),
   path('login/', views.login, name='login'),
   path('register/', views.register, name='register'),
   path('', views.index, name='index'),
   path('edit_profile/', views.edit_profile, name='edit_profile'),
   path('food_diary/', views.food_diary, name='food_diary'),
   path('exercise_diary/', views.exercise_diary, name='exercise_diary'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('get_dashboard_data', views.get_dashboard_data, name='get_dashboard_data'),
]
