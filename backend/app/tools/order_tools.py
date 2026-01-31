# backend/app/tools/order_tools.py

def get_order_by_id(orders, order_id: str, customer_id: str):
    for order in orders:
        if order["order_id"] == order_id and order["customer_id"] == customer_id:
            return order
    return None


def can_cancel_order(order: dict):
    """
    Check if an order is eligible for cancellation.
    """
    if order["order_status"] == "Placed":
        return True, "Order is eligible for cancellation."
    
    if order["order_status"] in ["Shipped", "Out for Delivery"]:
        return False, "The order has already been shipped and cannot be cancelled."
    
    if order["order_status"] == "Delivered":
        return False, "The order has already been delivered. You may initiate a return instead."
    
    if order["order_status"] == "Cancelled":
        return False, "This order is already cancelled."

    return False, "This order cannot be cancelled."


from datetime import datetime

def can_return_order(order: dict, products: list):
    """
    Check if an order is eligible for return.
    """

    if order["order_status"] != "Delivered":
        return False, "Only delivered orders can be returned."

    order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
    days_since_delivery = (datetime.now() - order_date).days

    if days_since_delivery > 30:
        return False, "The return window of 30 days has expired."

    for item in order["products"]:
        product = next(
            (p for p in products if p["product_id"] == item["product_id"]),
            None
        )
        if product and not product["return_eligible"]:
            return False, f"{product['product_name']} is not eligible for return."

    return True, "This order is eligible for return."


