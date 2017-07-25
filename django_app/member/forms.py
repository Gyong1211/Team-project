from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField

from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meat:
        model = MyUser
        fields = ('email',)

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Password 가 일치하지 않습니다")

            return password2

        def save(self, commit=True):
            user = super(MyUserCreationForm, self).save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            return user


class MyUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="비밀번호")

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_staff')

    def clean_password(self):
        return self.initial["password"]