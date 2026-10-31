from django.contrib import admin
from django.urls import path
from catalog import views
urlpatterns = [
    path('',views.home,name='home'),
    path('songs/',views.songs,name='songs'),
    path('photos/',views.photos,name='photos'),
    path('pictures/',views.photos,name='pictures'),
    path('concerts/',views.concerts,name='concerts'),
    path('admin/',admin.site.urls),
]
