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
from DareYou import views

urlpatterns = [
    path('',views.home,name='home'),
    path('create/',views.create,name='create'),
    path('select_un/',views.select_un,name='select_un'),
    path('select_q/',views.select_q,name='select_q'),
    path('dareshared/',views.DareSharedGenericAPIView.as_view(), name='dareshared'),
    #path('dareshared/<id>/',views.DareSharedGenericAPIView.as_view(), name='daresharedid'),
    path('dareshared/<id>/',views.playdareview, name='daresharedid'),
    path('quest/', views.QuestionsGenericAPIView.as_view(), name='quest'),
    path('quest/<int:id>/', views.QuestionsGenericAPIView.as_view(), name='questwithid'),
]
