from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  # Plant stuff
  path('plants/', views.plants_index, name='index'),
  path('plants/create/', views.PlantCreate.as_view(), name='plants_create'),
  path('plants/<int:pk>/update/', views.PlantUpdate.as_view(), name="plants_update"),
  path('plants/<int:pk>/delete/', views.PlantDelete.as_view(), name="plants_delete"),
  path('plants/<int:plant_id>/', views.plants_detail, name="detail"),
  # Watering stuff
  path('plants/<int:plant_id>/add_watering', views.add_watering, name='add_watering'),
  # Fertilizer
  path('fertilizers/', views.FertilizerList.as_view(), name="fertilizers_index"),
  path('fertilizers/<int:pk>/', views.FertilizerDetail.as_view(), name="fertilizers_detail"),
  path('fertilizers/create/', views.FertilizerCreate.as_view(), name="fertilizers_create"),
  path('fertilizers/<int:pk>/update/', views.FertilizerUpdate.as_view(), name="fertilizers_update"),
  path('fertilizers/<int:pk>/delete/', views.FertilizerDelete.as_view(), name="fertilizers_delete"),
  path('plants/<int:plant_id>/assoc_fertilizer/<int:fertilizer_id>/', views.assoc_fertilizer, name='assoc_fertilizer'),
  
  # Account stuff
  path('accounts/signup/', views.signup, name='signup'),
]
