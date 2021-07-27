"""voting_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', index, name="index"),
    path('home/', home, name='home'),
    path('login/', login, name="login"),
    path('iris_upload/', iris, name="iris_upload"),
    path('voter_profile/', profile, name='voter_profile'),
    path('poll/', poll, name='polling'),
    path('votes/<int:voterid>,<int:nomid>/', votes, name='votes'),
    path('result/', result, name='result'),
    path('success/', success, name='success'),
    path('oops/', oops, name='oops'),
    path('list/', voter_list, name='voters_list'),
    path('detect_person/',detect_person,name='detect_person'),
    path('election_result_calculation/', election_result_calculation, name='election_result_calculation'),
    path('election_result_view/', election_result_view, name='election_result_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


