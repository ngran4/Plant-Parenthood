from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import WateringForm

from .models import Plant, Fertilizer, Photo

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'plantparenthood22'

# VIEWS


def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')

# ---------------------- PLANTS ----------------------#


@login_required
def plants_index(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, 'plants/index.html', {'plants': plants})


@login_required
def plants_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    available_fertilizers = Fertilizer.objects.exclude(
        id__in=plant.fertilizers.all().values_list('id'))
    watering_form = WateringForm()
    return render(request, 'plants/detail.html', {'plant': plant, 'watering_form': watering_form, 'fertilizers': available_fertilizers})


class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = ['nickname', 'common_name', 'scientific_name',
              'care_difficulty', 'light_requirement', 'water_interval']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = ['nickname', 'common_name', 'scientific_name',
              'care_difficulty', 'light_requirement', 'water_interval']


class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = '/plants/'

# ---------------------- WATERING ---------------------- #


@login_required
def add_watering(request, plant_id):
    form = WateringForm(request.POST)
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
    return redirect('detail', plant_id=plant_id)


# ---------------------- LOGIN/SIGNUP ---------------------- #
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


# ---------------------- FERTILIZER ---------------------- #
class FertilizerList(ListView):
    model = Fertilizer


class FertilizerDetail(DetailView):
    model = Fertilizer


class FertilizerCreate(CreateView):
    model = Fertilizer
    fields = "__all__"


class FertilizerUpdate(UpdateView):
    model = Fertilizer
    fields = "__all__"


class FertilizerDelete(DeleteView):
    model = Fertilizer
    success_url = "/fertilizers/"


@login_required
def assoc_fertilizer(request, plant_id, fertilizer_id):
    plant = Plant.objects.get(id=plant_id)
    plant.fertilizers.add(fertilizer_id)
    return redirect('detail', plant_id=plant_id)


@login_required
def remove_fertilizer(request, plant_id, fertilizer_id):
    plant = Plant.objects.get(id=plant_id)
    plant.fertilizers.remove(fertilizer_id)
    return redirect('detail', plant_id=plant_id)


# ---------------------- PHOTOS ---------------------- #
@login_required
def add_photo(request, plant_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, plant_id=plant_id)
        except:
            print('An error occured uploading file to S3')
    return redirect('detail', plant_id=plant_id)
