from django.contrib import admin
from .models import Income, Category, PredefinedCategory, Expense
# Register your models here.


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount')
    list_display_links = ('amount',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_display_links = ('user', 'name')
    # search_fields = ('name','user')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount')
    list_display_links = ('title',)


admin.site.register(Income, IncomeAdmin)
admin.site.register(PredefinedCategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
