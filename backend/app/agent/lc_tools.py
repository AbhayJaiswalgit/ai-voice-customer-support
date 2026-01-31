from langchain.tools import tool
from app.tools.product_tools import search_products, get_product_details, get_product_faqs
from app.tools.order_tools import get_order_by_id, can_cancel_order, can_return_order
from app.tools.policy_tools import retrieve_policy_section
from app.utils.loaders import load_products, load_faqs, load_orders, load_policies

# Load datasets into memory once
PRODUCTS = load_products()
FAQS = load_faqs()
ORDERS = load_orders()
POLICIES = load_policies()
CUSTOMER_ID = "C0029"

@tool
def search_products_tool(query: str) -> str:
    """Search products by category, price, rating"""
    return str(search_products(PRODUCTS,query))


@tool
def product_details_tool(product_name: str) -> str:
    """Get details of a product"""
    return str(get_product_details(PRODUCTS,product_name))


@tool
def product_faq_tool(product_name: str) -> str:
    """Get FAQs for a product"""
    return str(get_product_faqs(FAQS,product_name))


@tool
def track_order_tool(order_id: str) -> str:
    """Track an order status using the Order ID (e.g., O0001)."""
    # Fix: Pass the ORDERS list and CUSTOMER_ID
    order = get_order_by_id(ORDERS, order_id, CUSTOMER_ID)
    return str(order) if order else "Order not found."


@tool
def return_check_tool(order_id: str) -> str:
    """Check if an order is eligible for return based on policy."""
    # Fix: Pass the ORDERS list, then the found order to the eligibility checker
    order = get_order_by_id(ORDERS, order_id, CUSTOMER_ID)
    if not order:
        return "Order not found."
    # can_return_order needs (order_dict, products_list)
    return str(can_return_order(order, PRODUCTS))


@tool
def policy_tool(query: str) -> str:
    """Answer questions about company return, refund, or delivery policies."""
    # Fix: Pass the POLICIES dictionary
    return str(retrieve_policy_section(POLICIES, query))


@tool
def cancel_order_tool(order_id: str) -> str:
    """
    Cancels an order if eligible. 
    Required input: order_id (e.g., 'O0001').
    """
    # Step 1: Find the order object first
    order = get_order_by_id(ORDERS, order_id, CUSTOMER_ID)
    
    if not order:
        return f"Error: Order {order_id} not found."

    # Step 2: Pass the ACTUAL order dictionary to the logic function
    # This prevents the TypeError you're seeing
    allowed, message = can_cancel_order(order)
    
    if allowed:
        # In a real app, you would update the JSON/DB here
        return f"Success: {message}"
    else:
        return f"Denied: {message}"