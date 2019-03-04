from django.contrib.auth import login, logout
from django.contrib.auth import login
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, RedirectView
from django.contrib.auth import authenticate
from .forms import SignUpForm, LoginForm

from ratelimit.mixins import RatelimitMixin


class IndexView(TemplateView):
    template_name = "sec/base.html"


class LogoutView(RedirectView):
    pattern_name = "login"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(RatelimitMixin, FormView):
    ratelimit_key = 'ip'
    ratelimit_method = 'POST'
    ratelimit_rate = '3/m'
    ratelimit_block = True

    form_class = LoginForm
    template_name = "user/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        password = form.cleaned_data["password"]
        username = form.cleaned_data["username"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Provide a valid username and/or password")
            return super().form_invalid(form)


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()

        categories = form.cleaned_data["categories"]
        user.profile.company = form.cleaned_data["company"]
        user.profile.categories.add(*categories)

        user.save()

        login(self.request, user)

        return HttpResponseRedirect(self.success_url)
