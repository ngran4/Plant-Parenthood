from django.db import models

# Create your models here.




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
    water_interval = models.IntegerField()

    def __str__(self):
        return f'{self.common_name}'