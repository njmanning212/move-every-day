from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from .models import Exercise

# Create your views here.

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

class ExerciseCreate(CreateView):
  model = Exercise
  fields = ['name', 'url', 'tempo', 'repetitions', 'rest', 'resistance', 'sets', 'fatigue_level', 'instructions', 'category']

  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse('exercise-detail', kwargs={'pk': self.object.pk})

class ExerciseDetail(DetailView):
  model = Exercise

def exercise_index(request):
  exercises = Exercise.objects.all()
  return render(request, 'exercise/index.html', { 'exercises': exercises })

class ExerciseUpdate(UpdateView):
  model = Exercise
  fields = ['name', 'url', 'tempo', 'repetitions', 'rest', 'resistance', 'sets', 'fatigue_level', 'instructions', 'category']

  def get_success_url(self):
    return reverse('exercise-detail', kwargs={'pk': self.object.pk})

class ExerciseDelete(DeleteView):
  model = Exercise
  success_url = '/exercises/'

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