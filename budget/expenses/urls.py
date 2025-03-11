from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),

    path('categories/', views.categories, name='categories'),
    path('select_category/', views.select_category, name='select_category'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('new_category/', views.new_category, name='new_category'),

    path('new_income/', views.new_income, name='new_income'),
    path('income/<int:income_id>/', views.income, name='income'),
    path('edit_income/<int:income_id>/', views.edit_income, name='edit_income'),
    path('delete_income/<int:income_id>/', views.delete_income, name='delete_income'),

    path('new_expense/<int:category_id>/', views.new_expense, name='new_expense'),
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('expense/<int:expense_id>/', views.expense, name='expense'),

]
