from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction 
from .models import Profile 

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Enter Email'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False, 
        help_text='Enter your phone number (e.g., +201012345678)',
        widget=forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Enter Phone Number'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Enter Username'}),
            'password': forms.PasswordInput(attrs={'class': 'input_text', 'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'input_text', 'placeholder': 'Confirm Password'}),
        }


    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit) 

        if commit:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data.get('phone_number')
            profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'input_text', 'placeholder': 'Email'})
    )

    class Meta:
        model = Profile
        fields = ['phone_number'] 
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input_text', 'placeholder': 'Phone Number'}),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            user_to_populate = self.instance.user
        elif self.user_instance:
            user_to_populate = self.user_instance
        else:
            user_to_populate = None

        if user_to_populate:
            self.fields['username'].initial = user_to_populate.username
            self.fields['email'].initial = user_to_populate.email


    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance and self.instance.user: 
            if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
                raise forms.ValidationError("This email address is already in use by another account.")
        elif User.objects.filter(email=email).exists(): 
             raise forms.ValidationError("This email address is already in use by another account.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance and self.instance.user:
            if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
                raise forms.ValidationError("This username is already taken.")
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


    @transaction.atomic 
    def save(self, commit=True):
        profile = super().save(commit=False) 

        user = profile.user 
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()
        return profile