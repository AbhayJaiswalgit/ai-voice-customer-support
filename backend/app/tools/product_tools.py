# backend/app/tools/product_tools.py

def search_products(
    products,
    category=None,
    min_price=None,
    max_price=None,
    min_rating=None
):
    results = []

    # Clean the category once
    if category:
        category = category.strip().lower()

    for product in products:
        product_category = product["category"].strip().lower()

        # 🔥 FIX 1 — fuzzy match instead of exact match
        if category and category not in product_category:
            continue

        if min_price and product["price"] < min_price:
            continue

        if max_price and product["price"] > max_price:
            continue

        if min_rating and product["rating"] < min_rating:
            continue

        results.append(product)

    # Sort by rating (highest first)
    results.sort(key=lambda x: x["rating"], reverse=True)

    return results



def get_product_details(products, product_name: str):
    product_name = product_name.strip().lower()

    for product in products:
        db_name = product["product_name"].strip().lower()

        # 🔥 fuzzy containment instead of exact equality
        if product_name in db_name or db_name in product_name:
            return product

    return None



def get_product_faqs(faqs, product_name: str):
    product_name = product_name.strip().lower()

    for item in faqs:
        db_name = item["product_name"].strip().lower()

        # 🔥 fuzzy containment match
        if product_name in db_name or db_name in product_name:
            return item.get("faqs", [])

    return []


