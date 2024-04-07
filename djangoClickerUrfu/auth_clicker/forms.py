from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    class Meta:
        model = User
        fields = ["username", "password"]

    def save(self, if_commit=True):
        psw = self.cleaned_data["password"]
        username = self.cleaned_data["username"]
        user = User.objects.create_user(username=username, password=psw)
        if if_commit:
            user.save()
        return user
