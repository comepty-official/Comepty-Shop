from django import forms
from .models import Product, ProductImage, ProductVideo, Comment, Tag, UserProductVideo, Report


class ProductForm(forms.ModelForm):
    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Add tags separated by commas (e.g. trending, sale, new)',
            'class': 'form-control tag-input',
        })
    )

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'affiliate_link', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your product...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'affiliate_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class ProductVideoForm(forms.ModelForm):
    class Meta:
        model = ProductVideo
        fields = ['video', 'caption']
        widgets = {
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video caption (optional)'}),
        }


class UserProductVideoForm(forms.ModelForm):
    class Meta:
        model = UserProductVideo
        fields = ['video', 'caption']
        widgets = {
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tell us about this product...'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Write a comment...',
            }),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional details...'}),
        }
