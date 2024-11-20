from django.urls import path
from . import views
from django.contrib.auth import views as Authviews

urlpatterns = [
    path('login/', Authviews.LoginView.as_view(template_name='login.html'), name="login"),
    path('register/', views.register, name='register'),
    path('logout/', Authviews.LogoutView.as_view(template_name='logout.html'), name="logout"),
]