from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

CATEGORIES = (
    ('C', 'Cervical'),
    ('T', 'Thoracic'),
    ('L', 'Lumbar'),
    ('S', 'Shoulders'),
    ('H', 'Hips'),
    ('K', 'Knees'),
    ('A', 'Ankles'),
    ('F', 'Feet'),
    ('O', 'Other'),
)

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    tempo = models.CharField(max_length=100)
    repetitions = models.CharField(max_length=100)
    rest = models.CharField(max_length=100)
    resistance = models.CharField(max_length=100)
    sets = models.CharField(max_length=100)
    fatigue_level = models.CharField(max_length=100)
    instructions = models.TextField(max_length=250)
    category = models.CharField(
        max_length=1,
        choices=CATEGORIES,
        default=CATEGORIES[0][0]
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
