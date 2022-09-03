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
    # Account stuff
    path('accounts/signup/', views.signup, name='signup'),
]
