from django.urls import path
from .views import upload_image
from . import views

urlpatterns = [
    path("upload/", upload_image, name="upload_image"),
    path('images/', views.get_all_images, name='get_all_images'),
]
