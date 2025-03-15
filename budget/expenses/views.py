from .models import Category, Expense
from .forms import Income, CategoryForm, ExpenseForm, IncomeForm
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from django.db.models import Sum
from django.utils.timezone import now
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict



data_month = now().strftime('%Y-%m')



def month_expenses(request, year, month):
    expenses = Expense.objects.filter(user=request.user, date__year=year, date__month=month)
    return expenses

def category_expenses(request, category, year, month):
    expenses = Expense.objects.filter(user=request.user, category=category, date__year=year, date__month=month)
    return expenses


def month_incomes(request, year, month):
    expenses = Income.objects.filter(user=request.user, date__year=year, date__month=month)
    return expenses


def index(request):
    return render(request, 'expenses/index.html')


@login_required
def home(request):
    date = request.GET.get('date') or now().strftime('%Y-%m')
    year, month = date.split('-')
    expenses = month_expenses(request, year, month).order_by('-date','-time')
    incomes = month_incomes(request, year, month).order_by('-date', '-time')
    total_expenses = expenses.aggregate(Sum('amount'))[
                 'amount__sum'] or 0
    total_income = incomes.aggregate(Sum('amount'))[
                 'amount__sum'] or 0
    balance = total_income - total_expenses
    data_list = defaultdict(list)
    for expense in expenses:
        data_list[expense.date].append({'type': 'expense', 'data': expense})
    for income in incomes:
        data_list[income.date].append({'type': 'income', 'data': income})
    full_data = dict(sorted(data_list.items(), reverse=True))

    context = {
        'date': date,
        'total_income': total_income,
        'full_data': full_data,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'balance': balance
    }
    return render(request, 'expenses/home.html', context)


@login_required
def categories(request):
    user_categories = Category.objects.filter(user=request.user)
    context = {'user_categories': user_categories}
    return render(request, 'expenses/categories.html', context)


@login_required
def select_category(request):
    user_categories = Category.objects.filter(user=request.user)
    context = {'user_categories': user_categories}
    return render(request, 'expenses/select_category.html', context)



@login_required
def category(request, category_id):
    date = request.GET.get('date') or now().strftime('%Y-%m')
    year, month = date.split('-')
    category = Category.objects.get(id=category_id)
    expenses = category_expenses(request, category, year, month).order_by('date')
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    expenses_list = defaultdict(list)
    for expense in expenses:
        expenses_list[expense.date].append(expense)
    expenses_date = dict(sorted(expenses_list.items(), reverse=True))
    context = {
        'date': date,
        'category': category,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'expenses_date': expenses_date
    }
    return render(request, 'expenses/category.html', context)


@login_required
def new_category(request):
    if request.method != 'POST':
        form = CategoryForm()
    else:
        try:
            form = CategoryForm(data=request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('categories')
        except IntegrityError:
            messages.error(request, 'Категория с таким названием уже существует.')
    context = {'form': form}
    return render(request, 'expenses/new_category.html', context)


def new_income(request):
    date = now().strftime('%Y-%m-%d')
    if request.method != 'POST':
        form = IncomeForm()
    else:
        form = IncomeForm(data=request.POST)
        if form.is_valid():
            new_income = form.save(commit=False)
            new_income.user = request.user
            new_income.date = request.POST['date']
            new_income.save()
            return redirect('home')
    context = {
        'form': form,
        'date': date
    }
    return render(request, 'expenses/new_income.html', context)


@login_required
def income(request, income_id):
    income = Income.objects.get(id=income_id)
    context = {'income' : income,
               }
    return  render(request, 'expenses/income.html', context)


@login_required
def edit_income(request, income_id):
    income = Income.objects.get(id=income_id)
    date = str(income.date)
    if request.method != 'POST':
        form = IncomeForm(instance=income)
    else:
        form = IncomeForm(instance=income, data=request.POST)
        if form.is_valid():
            new_income = form.save(commit=False)
            new_income.date = request.POST['date']
            new_income.save()
            return redirect('home')
    context = {
        'form': form,
        'date': date,
        'income': income,
    }
    return render(request, 'expenses/edit_income.html', context)


@login_required
def delete_income(request, income_id):
    income = Income.objects.get(id=income_id)
    income.delete()
    return redirect('home')


def check_category_owner(request, category):
    if category.user != request.user:
        raise Http404


@login_required
def new_expense(request, category_id):
    date = now().strftime('%Y-%m-%d')
    category = Category.objects.get(id=category_id)
    check_category_owner(request, category)
    if request.method != 'POST':
        form = ExpenseForm()
    else:
        form = ExpenseForm(data=request.POST)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.user = request.user
            new_expense.category = category
            new_expense.date = request.POST['date']
            new_expense.save()
            return redirect('home')
    context = {
        'form': form,
        'category': category,
        'date': date
    }
    return render(request,'expenses/new_expense.html', context)


@login_required
def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    category = expense.category
    date = str(expense.date)
    check_category_owner(request, category)
    if request.method != 'POST':
        form = ExpenseForm(instance=expense)
    else:
        form = ExpenseForm(instance=expense, data=request.POST)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.date = request.POST['date']
            new_expense.save()
            return redirect('home')
    context = {
        'form': form,
        'date': date,
        'expense': expense,
        'category': category,
    }
    return render(request, 'expenses/edit_expense.html', context)


@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    category = expense.category
    check_category_owner(request, category)
    expense.delete()
    return redirect('home')


@login_required
def expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    category = expense.category
    context = {'expense' : expense,
               'category': category
               }
    return  render(request, 'expenses/expense.html', context)



