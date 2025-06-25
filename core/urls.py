from django.urls import path
from .views import (
    CashFlowRecordListView, CashFlowRecordCreateView, CashFlowRecordUpdateView, CashFlowRecordDeleteView,
    StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView,
    TypeListView, TypeCreateView, TypeUpdateView, TypeDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    SubCategoryListView, SubCategoryCreateView, SubCategoryUpdateView, SubCategoryDeleteView,
    load_categories, load_subcategories
)

urlpatterns = [
    path('', CashFlowRecordListView.as_view(), name='cashflowrecord_list'),
    path('add/', CashFlowRecordCreateView.as_view(), name='cashflowrecord_add'),
    path('<int:pk>/edit/', CashFlowRecordUpdateView.as_view(), name='cashflowrecord_edit'),
    path('<int:pk>/delete/', CashFlowRecordDeleteView.as_view(), name='cashflowrecord_delete'),
    path('ajax/load-categories/', load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', load_subcategories, name='ajax_load_subcategories'),
    path('dict/status/', StatusListView.as_view(), name='status_list'),
    path('dict/status/add/', StatusCreateView.as_view(), name='status_add'),
    path('dict/status/<int:pk>/edit/', StatusUpdateView.as_view(), name='status_edit'),
    path('dict/status/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
    path('dict/type/', TypeListView.as_view(), name='type_list'),
    path('dict/type/add/', TypeCreateView.as_view(), name='type_add'),
    path('dict/type/<int:pk>/edit/', TypeUpdateView.as_view(), name='type_edit'),
    path('dict/type/<int:pk>/delete/', TypeDeleteView.as_view(), name='type_delete'),
    path('dict/category/', CategoryListView.as_view(), name='category_list'),
    path('dict/category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('dict/category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('dict/category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('dict/subcategory/', SubCategoryListView.as_view(), name='subcategory_list'),
    path('dict/subcategory/add/', SubCategoryCreateView.as_view(), name='subcategory_add'),
    path('dict/subcategory/<int:pk>/edit/', SubCategoryUpdateView.as_view(), name='subcategory_edit'),
    path('dict/subcategory/<int:pk>/delete/', SubCategoryDeleteView.as_view(), name='subcategory_delete'),
] 