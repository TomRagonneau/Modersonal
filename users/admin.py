from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import TblUserCreationForm, TblUserChangeForm
from .models import TblUser


class TblUserAdmin(UserAdmin):
    """Administration for TBL Users."""

    add_form = TblUserCreationForm
    form = TblUserChangeForm

    list_display = ('email', 'title', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('title', 'first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('user_permissions', 'is_staff', 'is_superuser', 'is_active')}),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('title', 'first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('user_permissions', 'is_staff', 'is_superuser', 'is_active')}),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ('last_login', 'date_joined',)


admin.site.register(TblUser, TblUserAdmin)
