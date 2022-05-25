from django.contrib import admin
from django.urls import path, include

from podcastsearcher import views

# as per clinic suggestion trying to use a single urls.py this time
urlpatterns = [
    path('', views.index, name="home"),
    path('admin/', admin.site.urls),
]
