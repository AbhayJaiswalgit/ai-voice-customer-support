# from langchain.tools import tool
# from app.tools.product_tools import search_products, get_product_details, get_product_faqs
# from app.tools.order_tools import get_order_by_id, can_cancel_order, can_return_order
# from app.tools.policy_tools import retrieve_policy_section
# from app.utils.loaders import load_products, load_faqs, load_orders, load_policies


# from pydantic import BaseModel, Field

# class OrderToolInput(BaseModel):
#     order_id: str = Field(description="The ID of the order, e.g., 'O0001'")
#     customer_id: str = Field(description="The ID of the customer, e.g., 'C0025'")

# @tool(args_schema=OrderToolInput)
# def return_check_tool(order_id: str, customer_id: str) -> str:
#     """Check if an order is eligible for return. Requires both order_id and customer_id."""
#     order = get_order_by_id(ORDERS, order_id, customer_id)
#     if not order:
#         return f"Order {order_id} not found for customer {customer_id}."
#     return str(can_return_order(order, PRODUCTS))

# # Load datasets into memory once
# PRODUCTS = load_products()
# FAQS = load_faqs()
# ORDERS = load_orders()
# POLICIES = load_policies()

# @tool
# def search_products_tool(query: str) -> str:
#     """Search products by category, price, rating"""
#     return str(search_products(PRODUCTS,query))


# @tool
# def product_details_tool(product_name: str) -> str:
#     """Get details of a product"""
#     return str(get_product_details(PRODUCTS,product_name))


# @tool
# def product_faq_tool(product_name: str) -> str:
#     """Get FAQs for a product"""
#     return str(get_product_faqs(FAQS,product_name))


# @tool
# def track_order_tool(order_id: str, customer_id: str) -> str:
#     """Track an order status. Requires the Order ID and the Customer ID."""
#     # Pass the customer_id dynamically instead of using a hardcoded constant
#     order = get_order_by_id(ORDERS, order_id, customer_id)
#     return str(order) if order else f"Order {order_id} not found for customer {customer_id}."


# @tool
# def return_check_tool(order_id: str, customer_id: str) -> str:
#     """Check if an order is eligible for return. Requires Order ID and Customer ID."""
#     order = get_order_by_id(ORDERS, order_id, customer_id)
#     if not order:
#         return f"Order {order_id} not found for customer {customer_id}."
#     return str(can_return_order(order, PRODUCTS))


# @tool
# def policy_tool(query: str) -> str:
#     """Answer questions about company return, refund, or delivery policies."""
#     # Fix: Pass the POLICIES dictionary
#     return str(retrieve_policy_section(POLICIES, query))


# @tool
# def cancel_order_tool(order_id: str, customer_id: str) -> str:
#     """Cancels an order if eligible. Requires Order ID and Customer ID."""
#     order = get_order_by_id(ORDERS, order_id, customer_id)
#     if not order:
#         return f"Error: Order {order_id} not found for customer {customer_id}."
    
#     allowed, message = can_cancel_order(order)
#     return f"Success: {message}" if allowed else f"Denied: {message}"

import json
from langchain.tools import tool
from app.tools.product_tools import search_products, get_product_details, get_product_faqs
from app.tools.order_tools import get_order_by_id, can_cancel_order, can_return_order
from app.tools.policy_tools import retrieve_policy_section
from app.utils.loaders import load_products, load_faqs, load_orders, load_policies
from app.agent.memory import get_session


# [cite_start]Load datasets into memory once [cite: 10]
PRODUCTS = load_products()
FAQS = load_faqs()
ORDERS = load_orders()
POLICIES = load_policies()

# --- HELPER: ROBUST JSON PARSER ---
def parse_json_input(input_text: str):
    """
    Robustly parse the input string into a dictionary.
    Handles extra quotes which Mistral sometimes adds.
    """
    try:
        # Clean up the input string (remove backticks or markdown quotes)
        cleaned_text = input_text.strip().strip("`").strip("'").strip('"')
        # If it's already a dictionary (unlikely but possible via some agents), return it
        if isinstance(input_text, dict):
            return input_text
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        # Fallback: If the LLM sends plain text, try to map it safely
        return {"error": "Invalid JSON", "raw_input": input_text}

# --- ROBUST TOOLS (Single Argument Pattern) ---

@tool
def search_products_tool(category: str) -> str:
    """
    Search products by category name (plain text).
    Example Action Input: Electronics
    """

    results = search_products(PRODUCTS, category=category)

    if not results:
        return "No products found in this category."

    # Only take top 5 for LLM readability
    top = results[:5]

    lines = []
    for p in top:
        lines.append(
            f"{p['product_name']} costs ₹{p['price']} "
            f"with rating {p['rating']} stars"
        )

    return "Here are some top products:\n" + "\n".join(lines)


@tool
def product_details_tool(product_name: str) -> str:
    """
    Get readable details of a product.
    Example Action Input: Vortex Camera Max
    """

    product = get_product_details(PRODUCTS, product_name)

    if not product:
        return f"I could not find a product named {product_name}."

    return (
        f"{product['product_name']} costs ₹{product['price']}, "
        f"has a rating of {product['rating']} stars from {product['review_count']} reviews. "
        f"Stock available: {product['stock_available']}. "
        f"Delivery in {product['delivery_time_days']} days. "
        f"{product['description']}"
    )


@tool
def product_faq_tool(product_name: str) -> str:
    """
    Provide structured FAQs for a product.
    """

    faqs = get_product_faqs(FAQS, product_name)

    # 🔥 Neutral, data-style response
    if not faqs:
        return f"{product_name} | FAQs: None available"

    lines = []
    for faq in faqs:
        lines.append(f"Q: {faq['question']} | A: {faq['answer']}")

    return "\n".join(lines)




@tool
def track_order_tool(order_id: str) -> str:
    """
    Track order status using only the order ID.
    """

    import app.agent.memory as memory

    session = memory.get_session(memory.ACTIVE_SESSION_ID)
    customer_id = session["customer_id"]

    order = get_order_by_id(ORDERS, order_id, customer_id)

    if not order:
        return "Order not found for your account."

    product_names = [p["product_name"] for p in order["products"]]

    return (
        f"Order {order['order_id']} placed on {order['order_date']} "
        f"is currently {order['order_status']}. "
        f"Products in this order: {', '.join(product_names)}."
    )



@tool
def return_check_tool(order_id: str) -> str:
    """
    Check if an order is eligible for return using only the order ID.
    Example Action Input: O0001
    """

    import app.agent.memory as memory

    session = memory.get_session(memory.ACTIVE_SESSION_ID)
    customer_id = session["customer_id"]

    order = get_order_by_id(ORDERS, order_id, customer_id)

    if not order:
        return "Order not found for your account."

    allowed, message = can_return_order(order, PRODUCTS)

    if not allowed:
        return f"Return not allowed: {message}"

    session["operational"]["pending_action"] = {
        "type": "return",
        "order_id": order_id
    }

    return (
        f"Your order {order_id} is eligible for return. "
        "Do you want me to initiate the return for you?"
    )


@tool
def cancel_order_tool(order_id: str) -> str:
    """
    Cancel an order using only the order ID.
    Example Action Input: O0001
    """

    import app.agent.memory as memory

    session = memory.get_session(memory.ACTIVE_SESSION_ID)
    customer_id = session["customer_id"]

    order = get_order_by_id(ORDERS, order_id, customer_id)

    if not order:
        return "Order not found for your account."

    allowed, message = can_cancel_order(order)

    if not allowed:
        return f"Cancellation not allowed: {message}"

    # 🔥 store intent in session
    session["operational"]["pending_action"] = {
        "type": "cancel",
        "order_id": order_id
    }

    return (
        f"Your order {order_id} is eligible for cancellation. "
        "Do you want me to cancel it for you?"
    )


@tool
def policy_tool(query: str) -> str:
    """Answer questions about return, refund, or delivery policies."""
    # Handle cases where agent sends JSON {"query": "return"} vs string "return"
    try:
        params = json.loads(query)
        actual_query = params.get("query", query)
    except:
        actual_query = query
        
    return str(retrieve_policy_section(POLICIES, actual_query))

@tool
def product_policy_tool(product_name: str) -> str:
    """
    Get return eligibility and warranty information for a product.
    Example Action Input: Vortex Camera Max
    """

    product = get_product_details(PRODUCTS, product_name)
    faqs = get_product_faqs(FAQS, product_name)

    if not product:
        return f"I could not find a product named {product_name}."

    # Return eligibility from catalog
    returnable = "Yes" if product["return_eligible"] else "No"

    # Warranty from FAQs
    warranty_info = "Not specified in FAQs."
    for faq in faqs:
        if "warranty" in faq["question"].lower():
            warranty_info = faq["answer"]

    return (
    f"{product['product_name']} return eligible: {returnable}. "
    f"Warranty information: {warranty_info}"
)
