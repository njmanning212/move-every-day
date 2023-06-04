from django.urls import path
from . import views


urlpatterns = [
  path('accounts/signup/', views.signup, name='signup'),
  path('', views.Home.as_view(), name='home'),
  path('exercises/create/', views.ExerciseCreate.as_view(), name='exercise-create'),
  path('exercises/<int:pk>/', views.ExerciseDetail.as_view(), name='exercise-detail'),
  path('exercises/', views.exercise_index, name='exercise-index'),
]