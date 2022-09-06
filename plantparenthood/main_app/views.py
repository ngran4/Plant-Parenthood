from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Authorization stuff
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import WateringForm

from .models import Plant, Fertilizer

from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

@login_required
def plants_index(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, 'plants/index.html', {'plants': plants})

@login_required
def plants_detail(request, plant_id):
  plant = Plant.objects.get(id=plant_id)
  available_fertilizers = Fertilizer.objects.exclude(id__in = plant.fertilizers.all().values_list('id'))
  watering_form = WateringForm()
  return render(request, 'plants/detail.html', {'plant': plant, 'watering_form': watering_form, 'fertilizers': available_fertilizers})

@login_required
def add_watering(request, plant_id):
    form = WateringForm(request.POST)
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
    return redirect('detail', plant_id=plant_id)

class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = ['nickname', 'common_name', 'scientific_name', 'care_difficulty', 'light_requirement', 'water_interval']
    success_url = '/plants/'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)


class PlantUpdate(LoginRequiredMixin, UpdateView):
  model = Plant
  fields = ['nickname', 'common_name', 'scientific_name', 'care_difficulty', 'light_requirement', 'water_interval']
  success_url = '/plants/'

class PlantDelete(LoginRequiredMixin, DeleteView):
  model = Plant
  success_url = '/plants/'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})