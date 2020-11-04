from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('short/', views.short, name='short'),
    path('info/', views.info, name='info'),
    path('generate/', views.generate, name='generate'),
    path('captcha/', views.captcha, name='captcha'),
    path('text/', views.text_transform, name='text'),
    path('image/', views.image_transform, name='image'),
    path('pdfs/', views.pdf_manipulate, name='pdfs'),
    path('scan/', views.scan, name='scan'),
    path('signup/', views.handleSignup, name='handleSignup'),
    path('login/', views.handleLogin, name='handleLogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('feedback/', views.feedback, name='feedback'),
    path('about/', views.about, name='about'),

]
urlpatterns += [
    path('robots.txt', TemplateView.as_view(template_name='home/robots.txt', content_type='text/plain'))
]
