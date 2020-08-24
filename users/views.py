from pathlib import Path

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .forms import TblUserCreationForm, TblAuthenticationForm

AUTHENTICATION_DIR = Path('registration')


class TblRegisterView(generic.CreateView):
    """Registration view of TBL Users."""

    form_class = TblUserCreationForm
    success_url = reverse_lazy('home')
    template_name = AUTHENTICATION_DIR / 'register.html'
    redirect_authenticated_user = False

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # If the user is authenticated, the registration view is not reachable.
        if self.redirect_authenticated_user and request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check "
                    "that your success URL doesn't point to a login page."
                )

            return HttpResponseRedirect(redirect_to)

        return super(TblRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # If the user's registration form is valid, the user should be dump into
        # the database and be logged in.
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class TblLoginView(LoginView):
    """Login view of TBL Users."""

    form_class = TblAuthenticationForm
    success_url = reverse_lazy('home')
    template_name = AUTHENTICATION_DIR / 'login.html'
