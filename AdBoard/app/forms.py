from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'description',
            'categories',
            'author'
        ]

    def clean(self):
        cleaned_data = super().clean()      # call the 'clean' method of the parent class
        description = cleaned_data.get('description')
        name = cleaned_data.get('name')
        if name == description:
            raise ValidationError({"name": "Name and Description must be different!"})
        if name[0].islower():
            raise ValidationError(
                "Name must begin with Capital letter"
            )
        if description[0].islower():
            raise ValidationError(
                "Description must begin with Capital letter"
            )
        return cleaned_data
