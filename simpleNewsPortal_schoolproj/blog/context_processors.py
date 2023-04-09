from .models import Category
from django.db.models import Count


def categories(request):
    categories = Category.objects.annotate(num_posts=Count('post'))
    return {'categories': categories}
