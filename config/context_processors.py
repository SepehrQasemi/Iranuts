from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone


def navigation(request):
    try:
        from Shop.models import Category

        featured_categories = list(Category.objects.order_by("name")[:4])
    except (OperationalError, ProgrammingError):
        featured_categories = []

    return {
        "featured_categories": featured_categories,
        "site_name": "IraNuts",
        "site_tagline": "A legacy Django storefront and inventory demo.",
        "current_year": timezone.now().year,
    }
