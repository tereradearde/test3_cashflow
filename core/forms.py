from django import forms
from .models import CashFlowRecord, Status, Type, Category, SubCategory

class CashFlowRecordForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = [
            'date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтрация категорий по выбранному типу
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                self.fields['category'].queryset = Category.objects.none()
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
        else:
            self.fields['category'].queryset = Category.objects.none()

        # Фильтрация подкатегорий по выбранной категории
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance.pk:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.category)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        # Валидация обязательных полей
        for field in ['amount', 'type', 'category', 'subcategory']:
            if not cleaned_data.get(field):
                self.add_error(field, 'Обязательное поле.')
        return cleaned_data 