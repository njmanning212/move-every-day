from django.urls import path
from . import views


urlpatterns = [
  path('accounts/signup/', views.signup, name='signup'),
  path('', views.Home.as_view(), name='home'),
  path('exercises/create/', views.ExerciseCreate.as_view(), name='exercise-create'),
  path('exercises/<int:pk>/', views.ExerciseDetail.as_view(), name='exercise-detail'),
  path('exercises/', views.exercise_index, name='exercise-index'),
  path('exercises/<int:pk>/update/', views.ExerciseUpdate.as_view(), name='exercise-update'),
  path('exercises/<int:pk>/delete/', views.ExerciseDelete.as_view(), name='exercise-delete'),
  path('exercises/search/', views.search, name='exercise-search'),
  path('exercises/<int:exercise_id>/add-photo/', views.add_photo, name='add-photo'),
]