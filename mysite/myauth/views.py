from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from .models import Profile
from django.utils.translation import gettext_lazy as _, ngettext


class HelloView(View):
    welcome = _('Welcome to Ashgabat')

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items')or 0
        items=int(items_str)
        products_line=ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line =products_line.format(count =items)

        return HttpResponse(
            f"<h1>{self.welcome}</h1>"
            f"\n<h2>{products_line}</h2>"
        )


class AboutMeView(TemplateView):
    template_name = 'myauth/about_me.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password)
        login(self.request, user)
        return response


def login_view(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {'error': "Invalid login credentials"})


#
# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy('myauth:login')


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


@user_passes_test(lambda user: user.is_authenticated)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['dictionary'] = 'spamegss'
    return HttpResponse('Session set')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('dictionary', 'default value')
    return HttpResponse(f"Session value: {value}")


class DictionaryView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"dictio": "nary", "spam": "eggs"})
