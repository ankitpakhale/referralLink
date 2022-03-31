from django.urls import path
from . import views

urlpatterns = [
    path('maindash/',views.MAINDASH,name='MAINDASH'),
    path('casignup/<str:ref_code>',views.SignupView,name='CASIGNUP'),
    path('',views.login,name='CALOGIN'),
    path('prsignup/<str:ref_code>',views.prSignupView,name='PRSIGNUP'),
    path('prlogin/',views.prlogin,name='PRLOGIN'),
    path('calogout/',views.userLogOut,name='CALOGOUT'),
    path('prlogout/',views.prLogOut,name='PRLOGOUT'),
    path('cadash/', views.dashboard, name='CADASHBOARD'),
    path('prdash/', views.PRdashboard, name='PRDASHBOARD'),

# -------------------------------------------------------------------------

    path('',views.index, name='index'),
    path('login/',views.login1, name='login'),
    path('signup/',views.signup1, name='signup'),    
    path('home/',views.home, name='home'),   
    path('contact/',views.contact, name='contact'),
    path('blog/',views.blog, name='blog'),
    path('faq/',views.faq, name='faq'),
    path('forget/',views.forget, name='forget'),
    path('myprofile/',views.myprofile, name='myprofile')
]
