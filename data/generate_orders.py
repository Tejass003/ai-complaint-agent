"""
data/generate_orders.py
Generates 100 realistic Indian e-commerce orders
and saves to data/orders.json
"""

import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_IN")

COMPANIES = ["Amazon", "Flipkart", "Meesho"]

PRODUCTS = {
    "Electronics": [
        ("OnePlus 12 Smartphone", 64999),
        ("boAt Airdopes 141", 1299),
        ("Samsung Galaxy S23", 74999),
        ("HP Laptop 15s", 54990),
        ("Realme Buds Wireless", 799),
        ("Canon EOS 1500D Camera", 34995),
        ("Apple iPhone 14", 79900),
        ("Mi Smart TV 43", 28999),
        ("JBL Bluetooth Speaker", 4999),
        ("Boat Rockerz 450", 1799),
    ],
    "Clothing": [
        ("Levi's 511 Jeans", 2499),
        ("Allen Solly Formal Shirt", 1299),
        ("Printed Kurti Set", 399),
        ("Nike Dri-FIT T-Shirt", 1995),
        ("Zara Floral Dress", 3999),
        ("Manyavar Kurta", 4999),
        ("H&M Hoodie", 2499),
        ("Peter England Trousers", 1799),
        ("W Ethnic Suit", 1499),
        ("UCB Polo T-Shirt", 1299),
    ],
    "Footwear": [
        ("Nike Air Max 90", 8995),
        ("Bata Formal Shoes", 2499),
        ("Puma Running Shoes", 3999),
        ("Woodland Boots", 4999),
        ("Crocs Classic Clog", 3499),
        ("Adidas Ultraboost", 12999),
        ("Red Tape Sneakers", 1999),
        ("Sparx Sports Shoes", 899),
    ],
    "Home & Kitchen": [
        ("Prestige Pressure Cooker", 1899),
        ("Philips Air Fryer", 6499),
        ("Milton Thermosteel Flask", 799),
        ("Bajaj Mixer Grinder", 2299),
        ("Pigeon Gas Stove", 3499),
        ("Crompton Ceiling Fan", 2199),
        ("Havells Iron", 1499),
        ("Cotton Bedsheet Set", 599),
    ],
    "Beauty": [
        ("Mamaearth Face Wash", 299),
        ("Lakme Eyeconic Kajal", 199),
        ("WOW Vitamin C Serum", 499),
        ("Biotique Bio Cream", 249),
        ("Nivea Body Lotion", 349),
    ]
}

PAYMENT_METHODS = ["UPI", "COD", "Credit Card", "Debit Card", "EMI", "Net Banking"]

def generate_orders(n: int = 100) -> list:
    orders = []
    used_ids = set()

    for i in range(n):
        # Unique order ID
        while True:
            order_id = f"ORD-{random.randint(1000, 9999)}"
            if order_id not in used_ids:
                used_ids.add(order_id)
                break

        # Random product
        category = random.choice(list(PRODUCTS.keys()))
        product_name, base_price = random.choice(PRODUCTS[category])

        # Slight price variation
        order_value = base_price + random.randint(-100, 500)
        order_value = max(99, order_value)

        # Dates
        order_date    = fake.date_time_between(start_date="-60d", end_date="-3d")
        is_delivered  = random.random() > 0.1
        delivery_date = None
        days_since    = None

        if is_delivered:
            delivery_days = random.randint(2, 7)
            delivery_date = order_date + timedelta(days=delivery_days)
            days_since    = (datetime.now() - delivery_date).days
            days_since    = max(0, days_since)

        # Company
        company = random.choice(COMPANIES)

        orders.append({
            "order_id":           order_id,
            "customer_name":      fake.name(),
            "customer_email":     fake.email(),
            "customer_phone":     fake.phone_number(),
            "customer_city":      fake.city(),
            "product_name":       product_name,
            "category":           category,
            "order_value":        order_value,
            "order_date":         order_date.strftime("%Y-%m-%d"),
            "delivery_date":      delivery_date.strftime("%Y-%m-%d") if delivery_date else None,
            "days_since_delivery": days_since,
            "is_delivered":       is_delivered,
            "payment_method":     random.choice(PAYMENT_METHODS),
            "company":            company,
        })

    return orders


if __name__ == "__main__":
    orders = generate_orders(100)

    with open("data/orders.json", "w") as f:
        json.dump(orders, f, indent=2)

    print(f"✅ Generated {len(orders)} orders")
    print(f"   Saved to data/orders.json")

    # Quick summary
    companies = {}
    categories = {}
    for o in orders:
        companies[o["company"]]   = companies.get(o["company"], 0) + 1
        categories[o["category"]] = categories.get(o["category"], 0) + 1

    print(f"\nBy company:")
    for k, v in companies.items():
        print(f"   {k}: {v} orders")

    print(f"\nBy category:")
    for k, v in categories.items():
        print(f"   {k}: {v} orders")