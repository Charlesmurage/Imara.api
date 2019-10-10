# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.forms import ModelForm
# from .models import CustomUser, Counties

# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['urban'].queryset = Urban.objects.none()

# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.Meta.fields

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['urban'].queryset = Urban.objects.none()

