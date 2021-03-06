"""LetsDare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.cb_home,name='cb_home'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('about_us/',views.about_us,name='about_us'),
    path('cb_create/',views.cb_create,name='cb_create'),
    path('cb_quiz_quest/',views.cb_quiz_quest,name='cb_quiz_quest'),
    path('create_quiz/',views.create_quiz,name='create_quiz'),
    path('user_cnfbox/<str:user_alias_id>/',views.user_cnfbox,name='user_cnfbox'),
    path('user_played_cnfbox/<str:user_alias_id>/',views.user_played_cnfbox,name='user_played_cnfbox'),
    path('play_q/<str:quiz_id>/',views.player,name='player'),
    path('play_quiz/<str:quiz_id>/',views.play_quiz,name='play_quiz'),
    path('result/<str:quiz_id>/',views.result,name='result'),
    path('result_view/<str:quiz_id>/',views.result_view,name='result_view'),

]
