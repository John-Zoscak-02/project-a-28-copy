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

    path('friends/', views.invites_received_view, name='friends'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all-profiles'),
    path('to-invite/', views.invite_profiles_list_view, name='invite-profiles-view'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('about-us/', views.about_us, name='about-us'),
    path('department/<str:dept>/', views.DeptDetailView.as_view(), name='dept_detail'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_view'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend'),
    path('friends/accept/', views.accept_invitation, name='accept-invite'),
    path('friends/reject/', views.reject_invitation, name='reject-invite'),
    path('search', views.search_page, name='search'),
    path('add-comment/<int:pk>/', views.add_comment, name='add-comment'),
]
