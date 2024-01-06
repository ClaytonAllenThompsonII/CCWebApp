from django.urls import path
from .views import views


urlpatterns = [
    path('inventory/', views.upload_image, name='inventory' )
]