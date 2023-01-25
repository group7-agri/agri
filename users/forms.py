from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Training, Message, Inquiry, CustomUser
import datetime
from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib import messages

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email','phone','username', 'password1', 'password2','status']
        labels = {
            'first_name': 'Full Name',
            'phone': 'Your personal number',

            'status': 'I am (eg: Farmer)',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'required': 'required', 'minlength':10}),
            'email': forms.EmailInput(attrs={'required': 'required', 'minlength':10}),
            
            'first_name': forms.TextInput(attrs={'placeholder': 'eg: John Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'eg: John@gmail.com', 'minlength':10}),
            'username': forms.TextInput(attrs={'placeholder': 'eg: John123', 'minlength':6}),
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
        fields = ['name', 'email', 'username','nid',
                  'location', 'bio', 'profile_image', 
                  'phone1','phone2', 'born']
        widgets = {
            
            'phone1': forms.TextInput(attrs={'placeholder': '+2507XXXXXXXX', 'minlength': 10}),
            
            'nid': forms.TextInput(attrs={'placeholder': 'Your National Id','required': 'required', 'minlength': 16, 'maxlength': 16}),
            'phone2': forms.TextInput(attrs={'placeholder': '+2507XXXXXXXX', 'minlength': 10}),
            'email': forms.TextInput(attrs={'required': 'required', 'minlength': 10}),
            'name': forms.TextInput(attrs={'required': 'required', 'minlength': 10}),
            'username': forms.TextInput(attrs={'required': 'required', 'minlength': 6}),
            'location': forms.TextInput(attrs={'placeholder': 'eg: Kigali, Nyarugenge','required': 'required', 'minlength': 10}),
            'bio': forms.Textarea(attrs={'required': 'required', 'minlength': 20}),
            
            'born': forms.DateInput(attrs={'required': 'required'}),
            
            # 'born': forms.SelectDateWidget(),
        }
        labels = {
            'born': 'Date of Birth (18+)',
            'name': 'Full Name',
            'phone1': 'Personal Number ',
            'nid': 'National ID',
            'phone2': 'Other Number',

        }
        widgets = {
             'born': forms.DateInput(attrs={'Placeholder': 'Year-Month-Day', 'type': 'date'}),
        }


    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('born')
        if dob:
            age = (date.today() - dob).days / 365.2425
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old.")
            return dob
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
             field.widget.attrs.update({'class': 'input'})
           


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        # fields = '__all__'
        fields = ['trainer', 'completed', 'certificate', 'link', 'description']
        exclude = ['owner']
       
        labels = {
        'completed': 'Completion Time (Before Today)',
        }
        widgets = {
             'completed': forms.DateInput(attrs={'Placeholder': 'Year-Month-Day', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        my_date = cleaned_data.get("completed")
        if my_date >= date.today():
            raise forms.ValidationError("Entered date should  be less than today.")

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            
            field.widget.attrs.update({'class': 'input'})
            field.widget.attrs.update({'required': 'required'})

              
 




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

        
        labels = {
        'email': 'Your personal email for communication',
        }
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Kindly describe the problem you encountered'}),
            'subject': forms.TextInput(attrs={'placeholder': 'What went wrong'}),
        }

    def __init__(self, *args, **kwargs):
        super(InquiryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
