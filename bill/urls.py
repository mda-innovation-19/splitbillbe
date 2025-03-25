from django.urls import path
from .views import *

urlpatterns = [
    path('create_bill', create_bill, name='create_bill'),
    path('get_bill_by_user_id/<int:user_id>', get_bill_by_user_id, name='get_bill_by_user_id'),
    path('delete_bill/<int:bill_id>', delete_bill, name='delete_bill'),
    path('create_split_bill', create_split_bill, name='create_split_bill'),
    path('get_split_bill_by_id/<int:split_bill_id>', get_split_bill_by_id, name='get_split_bill_by_id'),
]