from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject (Optional)'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'subject': 'Subject',
            'message': 'Your Message',
        }