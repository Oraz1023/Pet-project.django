from .views import (
    login_view,
    logout_view,

    get_cookie_view,
    get_session_view,

    set_cookie_view,
    set_session_view,
    # MyLogoutView,
    AboutMeView,
    RegisterView,
    DictionaryView,
    HelloView,

)
from django.urls import path
from django.contrib.auth.views import LoginView

app_name = 'myauth'

urlpatterns = [
    # path('login/', login_view, name='login'),
    path('login/', LoginView.as_view(template_name='myauth/login.html', redirect_authenticated_user=True, ),
         name='login'),
    path('logout/', logout_view, name='logout'),
    # path('logout/', MyLogoutView.as_view(), name='logout'),

    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),

    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),

    path("dictionary/", DictionaryView.as_view(), name="dictionary"),

    path('hello/', HelloView.as_view(), name='hello'),

]
