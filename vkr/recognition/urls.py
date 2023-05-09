from django.urls import path

from .views import index, upload_files

urlpatterns = [
    path('', index),
    path('upload_file/', upload_files),
    path('result/', upload_files)
    # path('list_files/', model)
]
