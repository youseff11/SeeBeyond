from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )

    class Meta:
        model = Profile
        fields = ['phone_number']

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

        # Set widget attributes for all fields.
        self.fields['username'].widget.attrs.update({'class': 'input_text'})
        self.fields['email'].widget.attrs.update({'class': 'input_text'}) # Removed 'readonly' here
        self.fields['phone_number'].widget.attrs.update({'class': 'input_text'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
            raise forms.ValidationError("This email address is already in use by another account.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()    
            profile.save() 
        return profile