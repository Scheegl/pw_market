from django import forms
from django.core.exceptions import ValidationError
from .models import Lots, Reply

class LotsForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Lots
        fields = [
            # 'site_user',
            'category_choice',
            'title',
            'description',
            'price',
        ]

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        if price > 0.0:
            raise ValidationError(
                'Цена не может быть нулевой!'
            )

        description = cleaned_data.get('description')
        if description is not None and len(description) < 20:
            raise ValidationError({
                'description': 'Добавьте описание'
            })

        return cleaned_data

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']