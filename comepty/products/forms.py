from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, Div, HTML
from .models import Product, ProductImage, Comment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'affiliate_link', 'category', 'tags', 'youtube_url', 'video_file', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Give your product an awesome title...', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your product in detail. What makes it special?', 'rows': 5, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'}),
            'affiliate_link': forms.URLInput(attrs={'placeholder': 'https://your-affiliate-link.com/product', 'class': 'form-control'}),
            'youtube_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/watch?v=...', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['price'].required = False
        self.fields['youtube_url'].required = False
        self.fields['video_file'].required = False
        self.fields['thumbnail'].required = False
        self.fields['tags'].required = False
        self.fields['tags'].help_text = 'Add comma-separated tags (e.g. wireless, bluetooth, audio)'


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Optional caption...', 'class': 'form-control form-control-sm'}),
            'order': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0}),
        }


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=4,
    max_num=10,
    can_delete=True,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts about this product...',
                'rows': 3,
                'class': 'form-control',
            })
        }
        labels = {'text': ''}
