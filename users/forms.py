from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Training, Message, Inquiry, CustomUser


from django import forms
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email','phone','username', 'password1', 'password2','status']
        labels = {
            'first_name': 'Names',
            'phone': 'Your personal number',
            'status': 'I am (eg: Farmer)',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'required': 'required'}),
            
            'first_name': forms.TextInput(attrs={'placeholder': 'eg: ARISTO DUSHIMIRIMANA'}),
            'email': forms.EmailInput(attrs={'placeholder': 'eg: aristo@gmail.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'eg: aristo123'}),
            'password1': forms.TextInput(attrs={'placeholder': 'eg: Enter passowrd you can remember'}),
            
            'phone': forms.TextInput(attrs={'placeholder': '+2507XXXXXXXX'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        
        for field_name in self.fields:
            self.fields[field_name].required = True



class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email', 'username',
                  'location', 'bio', 'profile_image', 
                  'phone1','phone2')
        widgets = {
            
            'phone1': forms.TextInput(attrs={'placeholder': '+2507XXXXXXXX'}),
            'phone2': forms.TextInput(attrs={'placeholder': '+2507XXXXXXXX'}),
        }
        labels = {
            'phone1': 'Second Number ',
            'phone2': 'Other Number',

        }
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = '__all__'
        exclude = ['owner']
        
       

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject','attachment', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class InquiryForm(ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'subject','attachment', 'body']

    def __init__(self, *args, **kwargs):
        super(InquiryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
