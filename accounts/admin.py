# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser, Major, Minor, Counties, Urban, Creator, Group, Membership

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = [CustomUser, Creator]
#     list_display = ['email', 'username']

# admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import (
    CustomUser,
    Creator,
    Counties,
    Urban,
    Major,
    Minor,
    Group,
    Membership
)


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom CustomUser model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Creator)
admin.site.register(Major)
admin.site.register(Minor)
admin.site.register(Counties)
admin.site.register(Urban)
admin.site.register(Group)
admin.site.register(Membership)