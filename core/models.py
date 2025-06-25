from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Status(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Название статуса'))

    class Meta:
        verbose_name = _('Статус')
        verbose_name_plural = _('Статусы')
        ordering = ['name']

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Название типа'))

    class Meta:
        verbose_name = _('Тип')
        verbose_name_plural = _('Типы')
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Название категории'))
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories', verbose_name=_('Тип'))

    class Meta:
        unique_together = ('name', 'type')
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.name} ({self.type})"

class SubCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Название подкатегории'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name=_('Категория'))

    class Meta:
        unique_together = ('name', 'category')
        verbose_name = _('Подкатегория')
        verbose_name_plural = _('Подкатегории')
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"

class CashFlowRecord(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name=_('Дата создания'))
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=_('Статус'))
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name=_('Тип'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Категория'))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name=_('Подкатегория'))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Сумма (руб.)'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Комментарий'))
    date = models.DateField(verbose_name=_('Дата операции'), help_text=_('Дата, к которой относится операция'))

    class Meta:
        verbose_name = _('Запись ДДС')
        verbose_name_plural = _('Записи ДДС')
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.date}: {self.amount} руб. ({self.category} / {self.subcategory})"

    def clean(self):
        # Валидация бизнес-правил на уровне модели
        if self.category.type_id != self.type_id:
            raise ValidationError(_('Категория не относится к выбранному типу.'))
        if self.subcategory.category_id != self.category_id:
            raise ValidationError(_('Подкатегория не относится к выбранной категории.'))
