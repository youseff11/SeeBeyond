from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import get_user_model
from .models import Profile 
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # إضافة حقل الإيميل لحقول التسجيل الافتراضية

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, 
                               help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    email = forms.EmailField(required=True, 
                             help_text='Required. Enter a valid email address.')

    class Meta:
        model = Profile # الفورم ده بيرتبط بموديل Profile
        fields = ['phone_number'] # الحقل الوحيد من موديل Profile اللي الفورم ده هيتعامل معاه بشكل مباشر

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if user_instance:
            self.fields['username'].initial = user_instance.username
            self.fields['email'].initial = user_instance.email
        elif self.instance and self.instance.user: # كـ احتياطي لو user_instance متبعتش بشكل مباشر
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

        self.fields['username'].widget.attrs.update({'class': 'input_text'})
        self.fields['email'].widget.attrs.update({'class': 'input_text', 'readonly': 'readonly'})
        self.fields['phone_number'].widget.attrs.update({'class': 'input_text'})


    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email'] # حتى لو readonly، بيتم معالجته

        if commit:
            user.save()      # نحفظ التغييرات على موديل اليوزر
            profile.save()   # نحفظ التغييرات على موديل البروفايل
        return profile