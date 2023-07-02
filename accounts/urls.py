from django.urls import path
from .views import *



urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('logedin/',LogedInView.as_view(),name='logedin'),
    path('ProfileEdit/<int:pk>',ProfileEdit.as_view(),name='ProfileEdit'),
    path('Profile/<int:pk>/',ProfileView.as_view(),name='profile'),
]