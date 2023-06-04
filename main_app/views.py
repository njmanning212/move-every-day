from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

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

class ExerciseList(ListView):
  model = Exercise
