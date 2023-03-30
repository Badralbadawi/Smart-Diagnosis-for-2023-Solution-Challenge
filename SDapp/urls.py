from django.urls import path
from . import views

urlpatterns =[
    path('', views.index , name='index'),
    path('Sign', views.Admin , name='Admin'),
    path('Doctor', views.Doctor , name='Doctor'),
    path('Dr_assient', views.Dr_assint , name='Dr_assint'),
    path('taa', views.ta , name='ta'),

]