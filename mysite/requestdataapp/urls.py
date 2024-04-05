from django.urls import path
from .views import *

app_name='requestdataapp'

urlpatterns=[
    path("get/", process_get_view, name="get_view"),
    path("bio/", user_form_view, name="user_form_view"),
    path("upload/", handle_file_upload, name="handle_file_upload"),

]