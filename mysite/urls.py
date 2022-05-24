from django.contrib import admin
from django.urls import path, include

from podcastsearcher import views

# app_name = "podcast"
urlpatterns = [
    path('', views.index, name="home"),
    #path('', include('podcastsearcher.urls', namespace='podcast')),
    path('admin/', admin.site.urls),
]
