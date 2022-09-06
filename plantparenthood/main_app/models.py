from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Fertilizer(models.Model):
    brand_name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=100)
    nutrient_balance = models.CharField(max_length=8)
    rec_freq = models.CharField(max_length=100)

DIFFICULTIES = (
    ('E', 'Easy'),
    ('M', 'Medium'),
    ('H', 'Hard'),
)

LIGHT = (
    ('L', 'Low Light'),
    ('I', 'Bright Indirect'),
    ('D', 'Direct')
)



class Plant(models.Model):
    nickname = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    care_difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTIES,
        default=DIFFICULTIES[0][0])
    light_requirement = models.CharField(
        max_length=1,
        choices=LIGHT,
        default=LIGHT[1][0])
    water_interval = models.IntegerField(
        help_text= "(Enter days between waterings)"
    )
    fertilizers = models.ManyToManyField(Fertilizer)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.common_name}'

class Watering(models.Model): 
    date = models.DateField()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)


