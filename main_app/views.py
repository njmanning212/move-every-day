from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Exercise, Photo
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'njman-move-every-day'


class Home(LoginView):
  template_name = 'home.html'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

class ExerciseCreate(LoginRequiredMixin, CreateView):
  model = Exercise
  fields = ['name', 'url', 'tempo', 'repetitions', 'rest', 'resistance', 'sets', 'fatigue_level', 'instructions', 'category']

  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse('exercise-detail', kwargs={'pk': self.object.pk})

class ExerciseDetail(LoginRequiredMixin, DetailView):
  model = Exercise

@login_required
def exercise_index(request):
  exercises = Exercise.objects.all()
  return render(request, 'exercise/index.html', { 'exercises': exercises })

class ExerciseUpdate(LoginRequiredMixin, UpdateView):
  model = Exercise
  fields = ['name', 'url', 'tempo', 'repetitions', 'rest', 'resistance', 'sets', 'fatigue_level', 'instructions', 'category']

  def get_success_url(self):
    return reverse('exercise-detail', kwargs={'pk': self.object.pk})

class ExerciseDelete(LoginRequiredMixin, DeleteView):
  model = Exercise
  success_url = '/exercises/'

@login_required
def search(request):
  search_term = request.GET.get('search')
  category = request.GET.get('category')
  if category == "All Exercises":
    exercises = Exercise.objects.filter(name__icontains=search_term)
  else:
    category = request.GET.get('category')[0]
    if category == 'M':
      exercises = Exercise.objects.filter(name__icontains=search_term, owner=request.user)
    else:
      exercises = Exercise.objects.filter(name__icontains=search_term, category=category)
  return render(request, 'exercise/index.html', { 'exercises': exercises})

@login_required
def add_photo(request, exercise_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, exercise_id=exercise_id)
      exercise_photo = Photo.objects.filter(exercise_id=exercise_id)
      if exercise_photo.first():
        exercise_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('exercise-detail', pk=exercise_id)