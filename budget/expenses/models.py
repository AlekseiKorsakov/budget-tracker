from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(auto_now_add=True, verbose_name=' Время')

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = "Доход за месяц"
        verbose_name_plural = "Доходы за месяц"

    @classmethod
    def get_month_incomes(cls, user, year, month):
        expenses = Income.objects.filter(user=user, date__year=year, date__month=month)
        return expenses

    @classmethod
    def get_month_income_amount(cls, user, year, month):
        return cls.get_month_incomes(user, year, month).aggregate(Sum('amount'))[
                'amount__sum'] or 0


class PredefinedCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предустановленная категория'
        verbose_name_plural = 'Предустановленные категории'


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Название')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Моя категория'
        verbose_name_plural = 'Мои категории'
        unique_together = ('user', 'name')


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(blank=True, null=True, max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(auto_now_add=True, verbose_name=' Время')

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name='Расходы'
        verbose_name_plural = 'Расходы'

    @classmethod
    def get_month_expenses(cls, user, year, month):
        return cls.objects.filter(user=user, date__year=year, date__month=month)

    @classmethod
    def get_category_expenses(cls, user, category, year, month):
        return cls.objects.filter(user=user, category=category, date__year=year, date__month=month)

    @classmethod
    def get_month_expenses_amount(cls, user, year, month):
        return cls.get_month_expenses(user, year, month).aggregate(Sum('amount'))[
                         'amount__sum'] or 0

    @classmethod
    def get_category_expenses_amount(cls, user, category, year, month):
        return cls.get_category_expenses(user, category, year, month).aggregate(Sum('amount'))[
            'amount__sum'] or 0