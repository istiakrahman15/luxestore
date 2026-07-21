from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product

# ---------------------------------------------------------------------------
# Admin branding — gives the Django admin a "LuxeStore" identity instead of
# the default "Django administration" chrome.
# ---------------------------------------------------------------------------
admin.site.site_header = "LuxeStore Admin"
admin.site.site_title = "LuxeStore Admin"
admin.site.index_title = "Catalog management"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "product_count_display")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    @admin.display(description="Products")
    def product_count_display(self, obj):
        return obj.product_count


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "name",
        "category",
        "price",
        "stock_toggle",
        "featured_toggle",
        "created_at",
    )
    list_display_links = ("thumbnail", "name")
    list_filter = ("category", "in_stock", "is_featured")
    search_fields = ("name", "description", "short_description")
    list_editable = ()
    ordering = ("-created_at", "price")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("image_preview", "created_at", "updated_at")
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic information", {
            "fields": ("name", "slug", "category", "price"),
        }),
        ("Description", {
            "fields": ("short_description", "description"),
        }),
        ("Image", {
            "fields": ("image", "image_preview"),
        }),
        ("Status", {
            "fields": ("in_stock", "is_featured"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Image")
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;object-fit:cover;'
                'border-radius:8px;" />',
                obj.image.url,
            )
        return format_html(
            '<div style="width:48px;height:48px;border-radius:8px;'
            'background:#eee;display:flex;align-items:center;justify-content:center;'
            'font-size:10px;color:#999;">No image</div>'
        )

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:260px;border-radius:12px;" />',
                obj.image.url,
            )
        return "No image uploaded yet."

    @admin.display(description="Stock", boolean=True, ordering="in_stock")
    def stock_toggle(self, obj):
        return obj.in_stock

    @admin.display(description="Featured", boolean=True, ordering="is_featured")
    def featured_toggle(self, obj):
        return obj.is_featured
