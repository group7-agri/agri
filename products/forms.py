from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Product, Review


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'featured_image', 'description','quantity','unity','price','location', 'payments']
        
        labels = {
            'quantity': 'Quantity ',
            'unity': 'Measurement',
            'price' : 'Initial Price(Rwf)'
        }

        widgets = {
            # 'payments': forms.CheckboxSelectMultiple(),
            'payments': forms.CheckboxSelectMultiple(attrs = {'class': 'input input--checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

       
         
        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})


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

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
