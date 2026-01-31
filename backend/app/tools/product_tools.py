# backend/app/tools/product_tools.py

def search_products(
    products,
    category=None,
    min_price=None,
    max_price=None,
    min_rating=None
):
    results = []

    for product in products:
        if category and product["category"].lower() != category.lower():
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
    for product in products:
        if product["product_name"].lower() == product_name.lower():
            return product
    return None


def get_product_faqs(faqs, product_name: str):
    for item in faqs:
        if item["product_name"].lower() == product_name.lower():
            return item.get("faqs", [])
    return []

