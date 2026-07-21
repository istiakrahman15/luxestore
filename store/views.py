from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    """Landing page: hero, featured products, categories, latest products."""
    featured_products = Product.objects.filter(is_featured=True).select_related("category")[:8]
    latest_products = Product.objects.select_related("category").order_by("-created_at")[:8]
    categories = Category.objects.all()[:5]

    context = {
        "featured_products": featured_products,
        "latest_products": latest_products,
        "categories": categories,
    }
    return render(request, "store/home.html", context)


def product_list(request):
    """Product catalog with search and category filtering."""
    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    context = {
        "products": products,
        "categories": categories,
        "query": query,
        "active_category": active_category,
        "result_count": products.count(),
    }
    return render(request, "store/product_list.html", context)


def product_detail(request, slug):
    """Single product page with a handful of related items."""
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(pk=product.pk)
        .select_related("category")[:4]
    )
    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "store/product_detail.html", context)


def about(request):
    return render(request, "store/about.html")


def contact(request):
    """Contact page. UI-only form — no backend submission by design."""
    return render(request, "store/contact.html")


def custom_404(request, exception=None):
    """Branded 404 page, wired up via `handler404` in settings.py."""
    return render(request, "store/404.html", status=404)
