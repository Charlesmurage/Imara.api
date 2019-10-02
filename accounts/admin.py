from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Major, Minor, Counties, Urban, Creator

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = [CustomUser, Creator]
    list_display = ['email', 'username']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Creator, CustomUserAdmin)
admin.site.register(Major)
admin.site.register(Minor)
admin.site.register(Counties)
admin.site.register(Urban)