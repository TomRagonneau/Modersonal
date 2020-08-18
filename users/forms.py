from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from .models import TblUser


class TblUserCreationForm(UserCreationForm):
    """Creation form of TBL Users."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # print only the name of the labels in the views
        super(TblUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TblUser
        fields = ('email', 'title', 'first_name', 'last_name',)


class TblAuthenticationForm(forms.Form):
    """Authentication form of TBL Users."""

    email = forms.EmailField(label=_('Email address'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    remember = forms.BooleanField(label=_('Remember me'), required=False, widget=forms.CheckboxInput())

    error_messages = {
        'invalid_login': _('Please enter a correct %(email)s and password. '
                           'Note that the password field may be case-sensitive.'),
        'inactive': _('This account is inactive.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        kwargs.setdefault('label_suffix', '')  # print only the name of the labels in the views
        super(TblAuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the 'email' field.
        UserModel = get_user_model()
        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

        # Place the auto-focus on the 'email' field.
        self.fields['email'].widget.attrs.update({'autofocus': True})

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                # During the authentication phase, it is primordial to ensure the existence of the user in the database
                # before raising any error if the authentication failed, to differentiate the inactive and invalid_login
                # errors.
                try:
                    user_profile = TblUser.objects.get(email=email)
                except ObjectDoesNotExist:
                    user_profile = None

                if user_profile is not None and user_profile.check_password(password):
                    self.confirm_login_allowed(user_profile)

                raise forms.ValidationError(
                    {'email': forms.ValidationError(
                        self.error_messages['invalid_login'],
                        params={'email': self.email_field.verbose_name}
                    )},
                    code='invalid_login',
                )

        if not self.cleaned_data.get('remember'):
            self.request.session.set_expiry(0)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class TblUserChangeForm(UserChangeForm):
    """Updating form of TBL Users."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # print only the name of the labels in the views
        super(TblUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TblUser
        fields = ('email', 'title', 'first_name', 'last_name',)
