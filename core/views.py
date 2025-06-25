from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CashFlowRecord, Status, Type, Category, SubCategory
from .forms import CashFlowRecordForm
from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

# Create your views here.

class CashFlowRecordListView(ListView):
    model = CashFlowRecord
    template_name = 'core/cashflowrecord_list.html'
    context_object_name = 'records'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        # Фильтрация по дате, статусу, типу, категории, подкатегории
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status = self.request.GET.get('status')
        type_ = self.request.GET.get('type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if status:
            qs = qs.filter(status_id=status)
        if type_:
            qs = qs.filter(type_id=type_)
        if category:
            qs = qs.filter(category_id=category)
        if subcategory:
            qs = qs.filter(subcategory_id=subcategory)
        return qs.select_related('status', 'type', 'category', 'subcategory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        return context

class CashFlowRecordCreateView(CreateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'core/cashflowrecord_form.html'
    success_url = reverse_lazy('cashflowrecord_list')

class CashFlowRecordUpdateView(UpdateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'core/cashflowrecord_form.html'
    success_url = reverse_lazy('cashflowrecord_list')

class CashFlowRecordDeleteView(DeleteView):
    model = CashFlowRecord
    template_name = 'core/cashflowrecord_confirm_delete.html'
    success_url = reverse_lazy('cashflowrecord_list')

def load_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).order_by('name')
    return JsonResponse(list(categories.values('id', 'name')), safe=False)

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)

# --- Миксин для справочников ---
class DictMixin:
    success_url = None
    template_prefix = ''
    def get_success_url(self):
        return self.success_url or reverse_lazy(f'{self.template_prefix}_list')
    def get_template_names(self):
        return [f'core/dict/{self.template_prefix}_form.html'] if self.template_name is None else [self.template_name]

# --- Status ---
class StatusListView(ListView):
    model = Status
    template_name = 'core/dict/status_list.html'
    context_object_name = 'objects'

class StatusCreateView(DictMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = None
    template_prefix = 'status'

class StatusUpdateView(DictMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = None
    template_prefix = 'status'

class StatusDeleteView(DictMixin, DeleteView):
    model = Status
    template_name = 'core/dict/status_confirm_delete.html'
    template_prefix = 'status'

# --- Type ---
class TypeListView(ListView):
    model = Type
    template_name = 'core/dict/type_list.html'
    context_object_name = 'objects'

class TypeCreateView(DictMixin, CreateView):
    model = Type
    fields = ['name']
    template_name = None
    template_prefix = 'type'

class TypeUpdateView(DictMixin, UpdateView):
    model = Type
    fields = ['name']
    template_name = None
    template_prefix = 'type'

class TypeDeleteView(DictMixin, DeleteView):
    model = Type
    template_name = 'core/dict/type_confirm_delete.html'
    template_prefix = 'type'

# --- Category ---
class CategoryListView(ListView):
    model = Category
    template_name = 'core/dict/category_list.html'
    context_object_name = 'objects'

class CategoryCreateView(DictMixin, CreateView):
    model = Category
    fields = ['name', 'type']
    template_name = None
    template_prefix = 'category'

class CategoryUpdateView(DictMixin, UpdateView):
    model = Category
    fields = ['name', 'type']
    template_name = None
    template_prefix = 'category'

class CategoryDeleteView(DictMixin, DeleteView):
    model = Category
    template_name = 'core/dict/category_confirm_delete.html'
    template_prefix = 'category'

# --- SubCategory ---
class SubCategoryListView(ListView):
    model = SubCategory
    template_name = 'core/dict/subcategory_list.html'
    context_object_name = 'objects'

class SubCategoryCreateView(DictMixin, CreateView):
    model = SubCategory
    fields = ['name', 'category']
    template_name = None
    template_prefix = 'subcategory'

class SubCategoryUpdateView(DictMixin, UpdateView):
    model = SubCategory
    fields = ['name', 'category']
    template_name = None
    template_prefix = 'subcategory'

class SubCategoryDeleteView(DictMixin, DeleteView):
    model = SubCategory
    template_name = 'core/dict/subcategory_confirm_delete.html'
    template_prefix = 'subcategory'
