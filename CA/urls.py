from os import name
from django.urls import path
from . import views

urlpatterns = [
            path('casignup/',views.SignupView,name='CASIGNUP'),
            path('calogin/',views.login,name='CALOGIN'),
            path('prsignup/',views.prSignupView,name='PRSIGNUP'),
            path('prlogin/',views.prlogin,name='PRLOGIN'),
            path('calogout/',views.userLogOut,name='CALOGOUT'),
            path('prlogout/',views.prLogOut,name='PRLOGOUT'),
            path('', views.dashboard, name='CADASHBOARD'),
            path('prdash/', views.PRdashboard, name='PRDASHBOARD'),
]