from django import forms
from django.core import validators
from django.contrib.auth.models import Group
from django.forms import ModelForm
from .models import *
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):
    images = MultiFileField(max_num=3, max_file_size=1024 * 1024 * 5)
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount', 'preview']



class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

# class ProductForm(forms.Form):
#     name= forms.CharField(max_length=100, )
#     price= forms.DecimalField(min_value=1,max_value=100000, decimal_places=2)
#     description= forms.CharField(
#         label='Product Description',
#         widget=forms.Textarea(attrs={'rows':5,'cols':'30'}),
#         validators=[validators.RegexValidator(
#             regex='great',
#             message="Field must contain word 'great'",
#         )]
#     )
