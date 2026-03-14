import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils.text import slugify
from django.contrib.auth import get_user_model
from store.models import Category, Product, Review

# Clear all existing data
Product.objects.all().delete()
Category.objects.all().delete()
Review.objects.all().delete()

print("Creating categories...")
cats = {}
for name, slug, emoji, order in [
    ('Aquarium Fishes', 'aquarium-fishes', '🐠', 1),
    ('Equipment',       'equipment',       '⚙️', 2),
    ('Fish Foods',      'fish-foods',      '🌿', 3),
    ('Live Plants',     'live-plants',     '🌱', 4),
    ('Medicine & Care', 'medicine-care',   '💊', 5),
    ('Aquariums & Bowls','aquariums-bowls','🏺', 6),
]:
    cats[slug] = Category.objects.create(
        name=name, slug=slug, emoji=emoji, sort_order=order
    )
    print(f"  ✅ {emoji} {name}")

print("\nCreating products...")
products = [
    # (name, category_slug, price, offer_price, weight_kg, featured, new_arrival, bestseller, description, care_tips)
    ('Molly Pair', 'aquarium-fishes', 20, None, 0.15, True, True, True,
     'Beautiful Molly fish pair — hardy, peaceful and perfect for community tanks.',
     'pH 7.5–8.5 · Temp 24–28°C · 20L+ tank · Change 30% water weekly'),

    ('Betta Male OMH', 'aquarium-fishes', 150, None, 0.10, True, True, True,
     'Premium Over-Half-Moon male Betta. Spectacular tail spread exceeding 180°.',
     'pH 6.5–7.5 · Temp 24–28°C · Keep alone · 5L+ tank · Weekly water change'),

    ('Betta Female', 'aquarium-fishes', 70, None, 0.10, True, False, False,
     'Healthy female Betta fish. Great for sorority tanks or breeding.',
     'pH 6.5–7.5 · Temp 24–28°C · Can be kept in groups · 15L+ tank'),

    ('Baby Flower Horn', 'aquarium-fishes', 120, 80, 0.20, True, True, True,
     'Adorable baby Flowerhorn cichlid. Hump developing, beautiful markings. Special offer!',
     'pH 7–8 · Temp 25–30°C · Aggressive — keep alone · 100L+ tank'),

    ('Red Tail Cat Fish', 'aquarium-fishes', 220, None, 0.30, False, True, False,
     'Stunning Red Tail Catfish. Deep black body with vivid red-orange tail.',
     'pH 6–7.5 · Temp 23–28°C · Grows very large · Keep with larger fish'),

    ('Royal Blue Betta Full Moon', 'aquarium-fishes', 120, None, 0.10, True, True, True,
     'Breathtaking Royal Blue Betta with perfect full-moon tail. Competition-grade.',
     'pH 6.5–7.5 · Temp 25–28°C · Keep alone · Weekly water change'),

    ('Royal Blood Red Betta', 'aquarium-fishes', 120, None, 0.10, True, True, True,
     'Stunning deep crimson Betta with lush full-moon tail. Show-quality fish.',
     'pH 6.5–7.5 · Temp 25–28°C · Keep alone · Carnivore diet'),

    ('Vinegar Eel Culture', 'aquarium-fishes', 80, None, 0.05, False, False, False,
     'Live Vinegar Eel starter culture. Excellent first food for Betta fry.',
     'Store at room temp · Feed apple cider vinegar · Split every 3 months'),

    ('Air Pump One Way', 'equipment', 99, None, 0.30, True, False, True,
     'Reliable single-outlet aquarium air pump. Quiet motor, adjustable flow.',
     'For tanks up to 60L · Includes air stone and tubing · Adjustable valve'),

    ('Siphon Pipe', 'equipment', 99, None, 0.20, False, False, False,
     'Manual gravel siphon for easy tank cleaning and water changes.',
     'For tanks 20–200L · Manual pump start · Gravel cleaning attachment'),

    ('4 Inch Fish Net', 'equipment', 50, None, 0.10, False, False, False,
     '4-inch aquarium catching net. Fine mesh prevents injury. Sturdy handle.',
     'Fine nylon mesh · Rust-proof frame · Suitable for small to medium fish'),

    ('Blue Medicine Anti Ich 5ml', 'medicine-care', 50, None, 0.05, False, False, False,
     'Dr. Ocean Anti-Ich treatment 5ml. Effective against white spot disease.',
     'Dose: 1ml per 10L · Remove carbon filter · Treat for 5–7 days'),

    ('Royal Betta Food', 'fish-foods', 110, None, 0.05, True, False, True,
     'Horizon Royal premium Betta food. Enhances color, promotes conditioning.',
     'Feed 2–3 pellets twice daily · High protein · Color-enhancing formula'),

    ('Champion Guppy Food 20g', 'fish-foods', 60, None, 0.02, True, False, False,
     'Champion Fancy Guppy premium food 20g. Enhances color and growth.',
     'Feed twice daily · Small granule size · Suitable for all small fish'),

    ('Champion Betta Food', 'fish-foods', 50, None, 0.02, True, False, False,
     'Champion brand Betta fish pellet food. Good color enhancement.',
     'Feed 3–4 pellets twice daily · High protein · Soak 30 sec before feeding'),

    ('Foxtail Plant', 'live-plants', 50, None, 0.05, True, False, False,
     'Myriophyllum aquaticum — gorgeous feathery plant. Excellent oxygenator.',
     'Low-medium light · No CO2 needed · Trim regularly · Great for breeding tanks'),

    ('Live Aquarium Plants Mix', 'live-plants', 50, None, 0.08, False, True, False,
     'Handpicked mix of live aquatic plants. Improves water quality naturally.',
     'Low to medium light · Fertilizer optional · Replant in substrate'),

    ('Artemia Capsule Brine Shrimp', 'medicine-care', 99, None, 0.05, False, False, False,
     'Pegon Artemia egg capsules. Hatch into live food within 24–36 hours.',
     'Hatch in salt water 25-35g/L · 25°C · 24–36 hrs · Rinse before feeding'),

    ('Almond Leaf', 'medicine-care', 30, None, 0.02, False, False, False,
     'Indian Almond Leaf. Natural Betta conditioner. Reduces pH, releases tannins, reduces stress.',
     '1 leaf per 10L · Soak first · Replace every 2 weeks'),

    ('Mini Aquarium', 'aquariums-bowls', 350, None, 1.50, True, False, False,
     'Complete mini aquarium setup. Compact acrylic tank — ideal for single Betta.',
     'Approx 3–5L · Rinse before use · Add dechlorinated water'),

    ('4 Inch Round Bowl', 'aquariums-bowls', 80, None, 0.80, False, False, False,
     'Classic 4-inch round fish bowl. Clear glass for excellent viewing.',
     'Approx 1–2L · Change water 2–3 times per week'),

    ('6 Inch Round Bowl', 'aquariums-bowls', 140, None, 1.20, False, False, False,
     'Spacious 6-inch fish bowl. More water volume for healthier fish.',
     'Approx 3–4L · Weekly 50% water change'),

    ('8 Inch Round Bowl', 'aquariums-bowls', 190, None, 1.80, False, False, False,
     'Large 8-inch fish bowl. Great for Betta with plants or decor.',
     'Approx 6–8L · Partial water change weekly'),

    ('Double Betta House', 'aquariums-bowls', 350, None, 1.00, True, False, False,
     'Dual-compartment Betta display house. Keep 2 Bettas separately in one unit.',
     'Two isolated compartments · Clear acrylic · Easy to clean'),

    ('Single Betta House', 'aquariums-bowls', 150, None, 0.60, True, False, False,
     'Individual Betta cup/house. Transparent acrylic. Great for display.',
     'Single compartment · Stackable design · Rinse before use'),
]

count = 0
for name, cat_slug, price, offer, weight, feat, new_arr, best, desc, care in products:
    slug = slugify(name)
    # Make unique if collision
    base = slug; i = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base}-{i}"; i += 1
    Product.objects.create(
        name=name, slug=slug, category=cats[cat_slug],
        price=price, offer_price=offer, weight_kg=weight,
        is_featured=feat, is_new_arrival=new_arr, is_bestseller=best,
        description=desc, care_tips=care, stock=50, is_active=True,
    )
    count += 1
    print(f"  ✅ {name}")

print("\nCreating reviews...")
for name, loc, rating, title, body in [
    ('Ravi Kumar', 'Chennai, TN', 5, 'Stunning fish!',
     'Ordered 3 Betta males. All arrived healthy and active. Colors are even better than photos. Perfect packaging!'),
    ('Priya Sharma', 'Nellore, AP', 5, 'Best fish store online',
     'Got Molly pairs and a Betta. Everything arrived safe. WhatsApp support was super helpful. Highly recommend!'),
    ('Karthik Raj', 'Coimbatore, TN', 4, 'Great quality, fast response',
     'Royal Blue Betta is gorgeous. Delivery on Monday as promised. Fish healthy and eating well same day.'),
    ('Sunita Devi', 'Vijayawada, AP', 5, 'Baby Flowerhorn thriving!',
     'Baby flower horn is growing beautifully. Very nice quality at amazing price!'),
    ('Arjun Reddy', 'Hyderabad, TS', 5, '5 Betta combo is worth it!',
     'Took the 5 Betta males combo for Rs.499 with free shipping. All 5 alive and healthy. Amazing value!'),
    ('Meena K', 'Madurai, TN', 5, 'Third order, always perfect!',
     'Never disappointed. Good oxygen packing. Fish survive transit perfectly. Will always shop here!'),
    ('Ganesh TN', 'Salem, TN', 4, 'Good packaging',
     'Fish survived transit well. Good oxygen packing. Siphon pipe working great.'),
    ('Lakshmi AP', 'Guntur, AP', 5, 'Will order every month!',
     'Artemia eggs hatched perfectly. Fry are eating well. Amazing seller on WhatsApp!'),
]:
    Review.objects.create(
        name=name, location=loc, rating=rating, title=title, body=body, verified=True
    )

# Admin user
U = get_user_model()
U.objects.filter(username='admin').delete()
U.objects.create_superuser('admin', 'admin@mvsaqua.com', 'mvsaqua2025')

print(f"""
{'='*50}
✅ {count} products created across {len(cats)} categories
✅ 8 customer reviews added
✅ Admin account: admin / mvsaqua2025
{'='*50}

Run the server:
  python manage.py runserver

Open in browser:
  Store : http://127.0.0.1:8000/
  Admin : http://127.0.0.1:8000/dashboard/login/
""")
