from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import PredefinedCategory, Category


# @receiver(post_migrate)
# def create_default_categories(sender, **kwargs):
#     default_categories = [
#         "Продукты", "Транспорт", "Жилье", "Здоровье", "Развлечения",
#         "Одежда", "Образование", "Путешествия", "Кафе и рестораны", "Прочее"
#     ]
#     for category in default_categories:
#         PredefinedCategory.objects.get_or_create(name=category)

@receiver(post_save, sender=User)
def create_user_categories(sender, instance, created, **kwargs):
    if created:
        predefined_categories = PredefinedCategory.objects.all()
        for category in predefined_categories:
            Category.objects.get_or_create(user=instance, name=category.name)