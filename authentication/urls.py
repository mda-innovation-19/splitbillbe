from django.urls import path
from .views import *

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('get_user_by_id/<int:user_id>', get_user_by_id, name='get_user_by_id'),
    path('get_user_by_account_number/<int:account_number>', get_user_by_account_number, name='get_user_by_account_number'),
    path('add_friend', add_friend, name='add_friend'),
    path('get_user_friends/<int:user_id>', get_user_friends, name='get_user_friends'),
]