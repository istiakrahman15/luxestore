from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """A product grouping, e.g. 'Watches' or 'Audio'."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short one-line description shown on the Categories section.",
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Bootstrap Icons class name, e.g. 'bi-smartwatch'.",
        default="bi-bag",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product_list") + f"?category={self.slug}"

    @property
    def product_count(self):
        return self.products.count()


class Product(models.Model):
    """A single item sold in the demo storefront."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField(
        help_text="Full product description shown on the detail page."
    )
    short_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Shown on product cards. Falls back to a trimmed description.",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    in_stock = models.BooleanField(
        default=True, help_text="Untick to show 'Out of Stock' on the storefront."
    )
    is_featured = models.BooleanField(
        default=False, help_text="Featured products appear on the homepage."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"slug": self.slug})

    @property
    def display_description(self):
        if self.short_description:
            return self.short_description
        if len(self.description) > 120:
            return self.description[:120] + "…"
        return self.description

    @property
    def stock_label(self):
        return "In Stock" if self.in_stock else "Out of Stock"
