from django.urls import path
from . import views


urlpatterns = [
    path('blog/',views.blog,name='blog'),
    path('',views.home,name='landing-page'),
]