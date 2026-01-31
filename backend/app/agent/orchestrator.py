# backend/app/agent/orchestrator.py

from app.agent.memory import get_session, update_session
from app.agent.intents import detect_intent
from app.tools.product_tools import (
    search_products,
    get_product_details,
    get_product_faqs
)
from app.utils.loaders import load_products, load_faqs
from app.tools.order_tools import get_order_by_id,can_cancel_order,can_return_order
from app.utils.loaders import load_orders,load_policies
from app.tools.policy_tools import retrieve_policy_section
import re


PRODUCTS = load_products()
FAQS = load_faqs()
ORDERS = load_orders()
POLICIES = load_policies()

# def extract_order_id(text: str):
#     match = re.search(r"O\d{4}", text)
#     return match.group(0) if match else None

# def resolve_product_name(products, raw_text: str):
#     raw_text = raw_text.lower()
#     for product in products:
#         if product["product_name"].lower() in raw_text:
#             return product["product_name"]
#     return None


# def process_message(session_id: str, message: str) -> str:
#     """
#     Central brain of the system.
#     """

#     # 1. Load session
#     session = get_session(session_id)

#     # 2. Detect intent
#     intent_result = detect_intent(message)
#     intent = intent_result["intent"]

#     # 3. Handle intent (very basic for now)
#     if intent == "SMALL_TALK":
#         response = "Hello! How can I help you today?"

#     elif intent == "PRODUCT_SEARCH":
#         filters = intent_result.get("filters", {})

#         results = search_products(
#             PRODUCTS,
#             category=filters.get("category"),
#             max_price=filters.get("max_price"),
#             min_rating=filters.get("min_rating")
#         )

#         if not results:
#             response = "I couldn’t find products matching your criteria. Would you like to adjust the filters?"
#         else:
#             lines = ["Here are some products you might like:"]
#             for p in results[:3]:
#                 lines.append(
#                     f"- {p['product_name']} (₹{p['price']}, ⭐ {p['rating']})"
#                 )
#             response = "\n".join(lines)

#     elif intent == "PRODUCT_DETAILS":
#         raw_name = intent_result.get("product_name")
#         product_name = resolve_product_name(PRODUCTS, raw_name)

#         if not product_name:
#             product_name = session.get("operational", {}).get("last_product")


#         if not product_name:
#             response = "Which product are you referring to?"
#         else:
#             product = get_product_details(PRODUCTS, product_name)

#             if not product:
#                 response = "I couldn’t find details for that product."
#             else:
#                 response = (
#                     f"{product['product_name']} costs ₹{product['price']}.\n"
#                     f"Rating: ⭐ {product['rating']} ({product['review_count']} reviews)\n"
#                     f"Stock available: {product['stock_available']}\n"
#                     f"Delivery time: {product['delivery_time_days']} days\n"
#                     f"Return eligible: {'Yes' if product['return_eligible'] else 'No'}\n\n"
#                     f"{product['description']}"
#                 )

#                 update_session(session_id, "last_product", product_name)

#     elif intent == "PRODUCT_FAQ":
#         raw_name = intent_result.get("product_name")
#         product_name = resolve_product_name(PRODUCTS, raw_name)

#         if not product_name:
#             product_name = session.get("operational", {}).get("last_product")


#         if not product_name:
#             response = "Which product are you asking about?"
#         else:
#             faqs = get_product_faqs(FAQS, product_name)

#             if not faqs:
#                 response = "I couldn’t find FAQ information for that product."
#             else:
#                 lines = ["Here are some common questions and answers:"]
#                 for faq in faqs:
#                     lines.append(f"Q: {faq['question']}\nA: {faq['answer']}")
#                 response = "\n\n".join(lines)

#                 update_session(session_id, "last_product", product_name)

#     elif intent == "ORDER_CANCEL":
#         customer_id = session.get("customer_id")
#         order_id = extract_order_id(message) or session.get("operational", {}).get("last_order_id")

#         if not order_id:
#             response = "Please provide your order ID to cancel the order."
#         else:
#             order = get_order_by_id(ORDERS, order_id, customer_id)

#             if not order:
#                 response = "I couldn’t find an order with that ID for your account."
#             else:
#                 allowed, reason = can_cancel_order(order)

#                 if not allowed:
#                     response = reason
#                 else:
#                     # Simulate cancellation
#                     order["order_status"] = "Cancelled"
#                     response = f"Your order {order_id} has been successfully cancelled."


#     elif intent == "ORDER_RETURN":
#         customer_id = session.get("customer_id")
#         order_id = extract_order_id(message) or session.get("operational", {}).get("last_order_id")

#         if not order_id:
#             response = "Please provide your order ID to check return eligibility."
#         else:
#             order = get_order_by_id(ORDERS, order_id, customer_id)

#             if not order:
#                 response = "I couldn’t find an order with that ID for your account."
#             else:
#                 allowed, reason = can_return_order(order, PRODUCTS)

#                 if not allowed:
#                     response = reason
#                 else:
#                     response = (
#                         f"Your order {order_id} is eligible for return.\n"
#                         "You can initiate a return by providing a reason."
#                     )

#     elif intent == "ORDER_TRACK":
#         customer_id = session.get("customer_id")
#         order_id = extract_order_id(message)

#         if not order_id:
#             response = "Please provide your order ID (e.g., O0002)."
#         else:
#             order = get_order_by_id(ORDERS, order_id, customer_id)

#             if not order:
#                 response = "I couldn’t find an order with that ID for your account."
#             else:
#                 product_names = [p["product_name"] for p in order["products"]]

#                 response = (
#                     f"Your order {order['order_id']} placed on {order['order_date']} is currently "
#                     f"**{order['order_status']}**.\n\n"
#                     f"Products in this order:\n- " + "\n- ".join(product_names)
#                 )

#                 update_session(session_id, "last_order_id", order_id)


#     elif intent == "POLICY_QUERY":
#         policy_text = retrieve_policy_section(POLICIES, message)

#         if not policy_text:
#             response = (
#                 "I can help with return, refund, cancellation, or delivery policies. "
#                 "Which one would you like to know about?"
#             )
#         else:
#             response = policy_text


#     else:
#         response = "Sorry, I didn’t understand that. Could you rephrase?"

#     # 4. Update session memory
#     update_session(session_id, "last_intent", intent)

#     return response

# from app.agent.agent_llm import run_agent
# from app.agent.llm_provider import llm

# def process_message(session_id: str, message: str):
#     session = get_session(session_id)

#     context = {
#         "products": PRODUCTS,
#         "orders": ORDERS,
#         "faqs": FAQS,
#         "policies": POLICIES,
#         "customer_id": session["customer_id"]
#     }

#     # 🔥 PHASE 5: DIRECT AGENT CALL (TEMP)
#     return run_agent(llm, message, context)

from app.agent.react_agent import agent_executor
from app.agent.memory import get_session, set_active_session

# backend/app/agent/orchestrator.py
# def process_message(session_id: str, message: str):
#       # 🔥 THIS LINE IS CRITICAL

#     session = get_session(session_id)
#     set_active_session(session_id) 
    
#     input_text = f"User (ID: {session['customer_id']}): {message}"
#     result = agent_executor.invoke({"input": input_text})
#     return result["output"]

def process_message(session_id: str, message: str):
    session = get_session(session_id)
    set_active_session(session_id)

    # 🔥 CHECK CONFIRMATION FIRST
    pending = session["operational"].get("pending_action")

    if pending and message.lower() in ["yes", "yes please", "confirm", "do it"]:
        order_id = pending["order_id"]

        if pending["type"] == "return":
            order = get_order_by_id(ORDERS, order_id, session["customer_id"])
            allowed, msg = can_return_order(order, PRODUCTS)
            session["operational"].pop("pending_action")
            return f"✅ Return initiated. {msg}"

        if pending["type"] == "cancel":
            order = get_order_by_id(ORDERS, order_id, session["customer_id"])
            allowed, msg = can_cancel_order(order)
            session["operational"].pop("pending_action")
            return f"✅ Order cancelled. {msg}"

    # normal agent flow
    input_text = f"User (ID: {session['customer_id']}): {message}"
    result = agent_executor.invoke({"input": input_text})
    return result["output"]

