from django.urls import path
from . import views

urlpatterns = [
    # path('',views.MAINDASH,name='MAINDASH'),

    path('prsignup/',views.prSignupView,name='PRSIGNUP'),
    path('prlogin/',views.prlogin,name='PRLOGIN'),
    path('prlogout/',views.prLogOut,name='PRLOGOUT'),
    path('', views.PRdashboard, name='PRDASHBOARD'),
    path('make_comp/', views.make_comp, name='make_comp'),
    path('payment/', views.payment, name='payment'),

    
]