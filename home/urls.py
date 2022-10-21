"""home URL Configuration

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
from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('friends', views.friends, name='friends'),
    path('profile', views.profile, name='profile'), # This will need to be a url in the form of {{username}}/profile this is temporary
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('department/<str:dept>', views.DeptDetailView.as_view(), name='dept_detail')
]
