from django.urls import path
from . import views


urlpatterns = [
  path('accounts/signup/', views.signup, name='signup'),
  path('', views.Home.as_view(), name='home'),
  path('exercises/create/', views.ExerciseCreate.as_view(), name='exercises-create'),
]