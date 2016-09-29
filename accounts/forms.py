from django import forms
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
	
from django.contrib.auth.forms import ReadOnlyPasswordHashField, authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from accounts.models import MyUser
User = get_user_model()

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_member')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


#gender_sex = (('1', 'male'), ('2', 'female'))


class UserRegisterForm(forms.Form):
    """docstring for UserRegisterForms"""
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email Address')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    #gender = forms.ChoiceField(label='Gender', widget=forms.Select, choices=gender_sex)

    class Meta:
        model = MyUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            #'gender',
        ]


    def clean_password2(self):
        # Check that the two password entries match
        minimum_length = 8
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password1) and len(password2) < minimum_length:
            raise ValidationError("password too short, password must contain at least a minimum of 8 characters and more.")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            exists = MyUser.objects.get(username=username)
            raise forms.ValidationError("USERNAME CONFLICT: Username already exists!, try another!")
        except MyUser.DoesNotExist:
            return username
        except:
            raise forms.ValidationError("An error occurred during registration process try again! or contact team-nerds ")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("EMAIL CONFLICT: Email already exists!, try another!")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("An error occurred during registration process try again! or contact team-nerds ")


class UserLoginForm(forms.Form):
    """docstring for UserLoginForm"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if username and password:
        	user = authenticate(username=username, password=password)
        	if not user:
        		raise forms.ValidationError("User match not found in database, try again with a valid user_id")

        	if not user.check_password(password):
        		raise forms.ValidationError("Incorrect pass-phrase")

        	if not user.is_active:
        		raise forms.ValidationError("User account for this user has been suspended, please contact admin primenerds")

        return super(UserLoginForm, self).clean(*args, **kwargs)
