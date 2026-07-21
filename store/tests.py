from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, Product


class CatalogModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Timepieces")
        self.product = Product.objects.create(
            name="Test Watch",
            category=self.category,
            description="A watch used in tests.",
            price="199.00",
        )

    def test_slugs_are_auto_generated(self):
        self.assertEqual(self.category.slug, "timepieces")
        self.assertEqual(self.product.slug, "test-watch")

    def test_stock_label_reflects_in_stock_flag(self):
        self.assertEqual(self.product.stock_label, "In Stock")
        self.product.in_stock = False
        self.product.save()
        self.assertEqual(self.product.stock_label, "Out of Stock")


class StoreViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Audio")
        self.product = Product.objects.create(
            name="Test Speaker",
            category=self.category,
            description="A speaker used in tests.",
            price="99.00",
            is_featured=True,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("store:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Speaker")

    def test_product_list_search(self):
        response = self.client.get(reverse("store:product_list"), {"q": "Speaker"})
        self.assertContains(response, "Test Speaker")

    def test_product_list_search_no_results(self):
        response = self.client.get(reverse("store:product_list"), {"q": "Nonexistent"})
        self.assertNotContains(response, "Test Speaker")

    def test_product_detail_page(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "99.00")

    def test_category_filter(self):
        other_category = Category.objects.create(name="Home Objects")
        Product.objects.create(
            name="Other Product",
            category=other_category,
            description="Unrelated item.",
            price="10.00",
        )
        response = self.client.get(reverse("store:product_list"), {"category": "audio"})
        self.assertContains(response, "Test Speaker")
        self.assertNotContains(response, "Other Product")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_custom_404_page(self):
        response = self.client.get("/this-page-does-not-exist/")
        self.assertContains(response, "shelf is empty", status_code=404)
