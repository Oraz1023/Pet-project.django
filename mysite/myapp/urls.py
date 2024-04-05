
from django.urls import reverse, path
from .views import *


app_name="myapp"

urlpatterns = [
    path("hello/", hello_world_view, name="hello"),
    path("groups/", GroupListView.as_view(),name="groups"),

]