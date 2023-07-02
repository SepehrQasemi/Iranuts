from django.urls import path
from .views import PostView,PostDetails,PostCreate,PostDelete,PostEdit

urlpatterns = [
    path('blog/',PostView.as_view() , name='Blog'),
    path('blog/Post/<int:pk>',PostDetails.as_view(), name = 'PostDetails'),
    path('new_post/',PostCreate.as_view(), name='PostCreate'),
    path('PostEdit/<int:pk>/',PostEdit.as_view(), name='PostEdit'),
    path('PostDelete/<int:pk>/',PostDelete.as_view(), name='PostDelete'),
    
]
