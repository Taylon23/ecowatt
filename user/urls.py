from django.urls import path
from . import views
from django.contrib.auth import views as AuthViews

urlpatterns = [
    path('login/', AuthViews.LoginView.as_view(template_name='login.html'), name="login"),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', AuthViews.LogoutView.as_view(), name="logout"),
]
