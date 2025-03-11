from django import forms
from datetime import datetime
from .models import Income, Expense, Category, PredefinedCategory






class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields =['description', 'amount']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['name']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']
