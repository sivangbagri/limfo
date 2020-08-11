from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('short/', views.short, name='short'),
    path('info/', views.info, name='info'),
    path('qrCode/', views.qrCode, name='qrCode'),
    path('translate/', views.translate, name='translate'),
    path('captcha/', views.captcha, name='captcha'),
    path('spell/', views.spell, name='spell'),
    path('bar_code/', views.bar_code, name='bar_code'),
    path('filter/', views.filter, name='filter'),
    path('covid/', views.covid_19, name='covid_19'),
    path('joke/', views.joke, name='joke'),
    path('signup/', views.handleSignup, name='handleSignup'),
    path('login/', views.handleLogin, name='handleLogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),

]
