from django.urls import path
from api.views import index, get_all_post, create_post, delete, get_post, update_post

urlpatterns = [
    path('api/', index),
    path('api/get_all_post/', get_all_post),
    path('api/create_post/', create_post),
    path('api/delete/', delete),
    path('api/get_post/', get_post),
    path('api/update_post/', update_post),

]
