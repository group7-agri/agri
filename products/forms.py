from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Product, Review


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'featured_image', 'description','quantity','location', 'payments']
        
        labels = {
            
            'name': 'Product Name',
            'quantity': 'Quantiy (in Kilogram, Litre....)',
            'featured_image': 'Product Image',
        }

        widgets = {
            # 'payments': forms.CheckboxSelectMultiple(),
            'payments': forms.CheckboxSelectMultiple(attrs = {'class': 'input input--checkbox'}),
            'featured_image': forms.FileInput(attrs = {'required': 'required'}),
            'description': forms.Textarea(attrs = {'required': 'required','minlength': 20}),
            'quantity': forms.TextInput(attrs = {'required': 'required'}),
            'location': forms.TextInput(attrs = { 'placeholder': 'eg: Kigali, Nyarugenge', 'required': 'required'}),
        }
    
    exclude_fields = {'payments'}
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            


        for field_name in self.fields:
            if field_name not in self.exclude_fields:
                self.fields[field_name].required = True
       
         
        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})
class TraderProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['featured_image', 'description','quantity','location', 'payments']
        
        
        labels = {
            
            'quantity': 'Quantiy (in Kilogram, Litre....)',
            'featured_image': 'Product Image',
        }

        widgets = {
            # 'payments': forms.CheckboxSelectMultiple(),
            'payments': forms.CheckboxSelectMultiple(attrs = {'class': 'input input--checkbox'}),
            'location': forms.TextInput(attrs = {'required': 'required', 'placeholder': 'eg: Kigali, Nyarugenge'}),
        }
    exclude_fields = {'payments'}
    

    def __init__(self, *args, **kwargs):
        super(TraderProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # for name, field in ['name', 'featured_image', 'description','quantity', 'location' ]:
        #     self.fields[field].required = True

        for field_name in self.fields:
            if field_name not in self.exclude_fields:
                self.fields[field_name].required = True

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['value'].required = True
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
