"""
Seeds the database with demo categories and products so the storefront
looks complete immediately after `migrate`.

Usage:
    python manage.py seed_demo_data
    python manage.py seed_demo_data --flush   # wipe existing catalog first
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from store.models import Category, Product

CATEGORIES = [
    {
        "name": "Timepieces",
        "description": "Mechanical and quartz watches, built to outlast trends.",
        "icon": "bi-smartwatch",
    },
    {
        "name": "Audio",
        "description": "Headphones and speakers tuned for honest sound.",
        "icon": "bi-boombox",
    },
    {
        "name": "Leather Goods",
        "description": "Full-grain leather bags and accessories.",
        "icon": "bi-briefcase",
    },
    {
        "name": "Home Objects",
        "description": "Considered pieces for the desk and the table.",
        "icon": "bi-cup-hot",
    },
    {
        "name": "Eyewear",
        "description": "Acetate and titanium frames, hand-finished.",
        "icon": "bi-eyeglasses",
    },
]

PRODUCTS = [
    # Timepieces
    dict(name="Meridian Automatic", category="Timepieces", price="428.00",
         short="Swiss automatic movement in a brushed steel case.",
         desc="The Meridian Automatic pairs a 41mm brushed stainless case with a "
              "sapphire crystal and a 42-hour power reserve. A quiet, precise "
              "companion for daily wear.", featured=True, stock=True),
    dict(name="Solstice Chronograph", category="Timepieces", price="512.00",
         short="Three-register chronograph with a tachymeter bezel.",
         desc="Solstice brings motorsport styling to the wrist with a fully "
              "functional chronograph, luminous hands, and a quick-release strap.",
         featured=False, stock=True),
    dict(name="Aline Minimal", category="Timepieces", price="219.00",
         short="A clean two-hand dial with a vegan leather strap.",
         desc="Aline strips the watch back to essentials: a domed crystal, a "
              "matte dial, and a strap made from apple-leather composite.",
         featured=False, stock=True),
    dict(name="Northbound Field Watch", category="Timepieces", price="265.00",
         short="Rugged field watch with a scratch-resistant case.",
         desc="Built for travel, Northbound has a matte titanium case, a "
              "high-contrast dial, and an interchangeable NATO strap.",
         featured=False, stock=False),

    # Audio
    dict(name="Aria Over-Ear Headphones", category="Audio", price="349.00",
         short="Closed-back headphones with memory-foam ear cups.",
         desc="Aria delivers a warm, balanced sound signature with 40mm "
              "drivers, active noise cancellation, and 30 hours of playback.",
         featured=True, stock=True),
    dict(name="Ember Wireless Earbuds", category="Audio", price="189.00",
         short="True wireless earbuds with adaptive EQ.",
         desc="Ember auto-tunes itself to your ear shape for consistent bass "
              "and clarity, with a matte-ceramic charging case.",
         featured=True, stock=True),
    dict(name="Cast Tabletop Speaker", category="Audio", price="299.00",
         short="A single-driver speaker with a walnut enclosure.",
         desc="Cast fills a room evenly from a compact walnut cabinet, with a "
              "capacitive touch dial for volume and source switching.",
         featured=False, stock=True),
    dict(name="Drift Portable Speaker", category="Audio", price="149.00",
         short="Splash-resistant speaker built for travel.",
         desc="Drift is rated IPX5 and fits in a jacket pocket, with 14 hours "
              "of battery life and a fabric-wrapped shell.",
         featured=False, stock=True),

    # Leather Goods
    dict(name="Harbor Weekender Bag", category="Leather Goods", price="398.00",
         short="Full-grain leather duffel with brass hardware.",
         desc="Harbor is hand-stitched from a single hide, with a canvas "
              "interior, a detachable shoulder strap, and space for a two-day trip.",
         featured=True, stock=True),
    dict(name="Fold Card Wallet", category="Leather Goods", price="68.00",
         short="A slim wallet that holds six cards and folded cash.",
         desc="Fold is cut from vegetable-tanned leather that darkens "
              "beautifully with age, finished with hand-burnished edges.",
         featured=False, stock=True),
    dict(name="Ledger Portfolio", category="Leather Goods", price="145.00",
         short="A5 leather portfolio with a magnetic closure.",
         desc="Ledger holds a notebook, loose pages, and a pen loop behind a "
              "magnetic flap, wrapped in pebbled leather.",
         featured=False, stock=True),
    dict(name="Waylon Belt", category="Leather Goods", price="79.00",
         short="A reversible belt with a brushed steel buckle.",
         desc="Waylon switches between black and chestnut with a twist of the "
              "buckle, cut from a single strip of full-grain leather.",
         featured=False, stock=False),

    # Home Objects
    dict(name="Pour Over Carafe Set", category="Home Objects", price="86.00",
         short="Borosilicate carafe with a walnut collar.",
         desc="A slow, deliberate way to make coffee: a hand-blown carafe, a "
              "reusable steel filter, and a walnut base that doubles as a trivet.",
         featured=True, stock=True),
    dict(name="Anchor Desk Lamp", category="Home Objects", price="132.00",
         short="A dimmable task lamp with a marble base.",
         desc="Anchor casts warm, even light through a spun-aluminum shade, "
              "with a touch-dimmer built into a solid marble base.",
         featured=False, stock=True),
    dict(name="Grove Ceramic Mug Set", category="Home Objects", price="54.00",
         short="Set of two stoneware mugs, glazed by hand.",
         desc="Each Grove mug is glazed individually, so no two are quite "
              "alike. Dishwasher and microwave safe despite the handmade finish.",
         featured=False, stock=True),
    dict(name="Fold Wool Throw", category="Home Objects", price="118.00",
         short="A lambswool throw, woven in a houndstooth check.",
         desc="Woven from lambswool on a traditional loom, Fold is heavy "
              "enough for cool evenings and finished with a fringed edge.",
         featured=False, stock=True),

    # Eyewear
    dict(name="Percy Round Frames", category="Eyewear", price="175.00",
         short="Hand-polished acetate frames with a keyhole bridge.",
         desc="Percy is cut from Italian acetate and finished by hand, with "
              "spring hinges for a comfortable, forgiving fit.",
         featured=True, stock=True),
    dict(name="Dune Sunglasses", category="Eyewear", price="210.00",
         short="Titanium sunglasses with polarized lenses.",
         desc="Dune pairs a featherweight titanium frame with polarized, "
              "UV400 lenses in a gradient tortoise finish.",
         featured=False, stock=True),
    dict(name="Vista Reading Glasses", category="Eyewear", price="95.00",
         short="Lightweight readers with a blue-light filter.",
         desc="Vista is built for screen time, with a blue-light filtering "
              "coating and a flexible titanium core inside the temples.",
         featured=False, stock=True),
]


class Command(BaseCommand):
    help = "Seeds the database with demo categories and products for LuxeStore."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing products and categories before seeding.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing catalog."))

        category_map = {}
        created_categories = 0
        for cat in CATEGORIES:
            obj, created = Category.objects.get_or_create(
                name=cat["name"],
                defaults={"description": cat["description"], "icon": cat["icon"]},
            )
            category_map[cat["name"]] = obj
            created_categories += created

        created_products = 0
        for p in PRODUCTS:
            _, created = Product.objects.get_or_create(
                name=p["name"],
                defaults={
                    "category": category_map[p["category"]],
                    "price": Decimal(p["price"]),
                    "short_description": p["short"],
                    "description": p["desc"],
                    "is_featured": p["featured"],
                    "in_stock": p["stock"],
                },
            )
            created_products += created

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created_categories} categories and "
            f"{created_products} products created "
            f"({Category.objects.count()} categories, "
            f"{Product.objects.count()} products total)."
        ))
