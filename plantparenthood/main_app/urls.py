from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # Plant stuff
    path('plants/', views.plants_index, name='index'),
    path('plants/create/', views.PlantCreate.as_view(), name='plants_create'),
    # Account stuff
    path('accounts/signup/', views.signup, name='signup'),

]
