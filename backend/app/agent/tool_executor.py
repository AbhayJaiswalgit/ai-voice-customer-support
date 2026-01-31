from app.tools.product_tools import *
from app.tools.order_tools import *
from app.tools.policy_tools import *

def execute_tool(tool_name: str, args: dict, context: dict):

    if tool_name == "search_products":
        return search_products(context["products"], **args)

    if tool_name == "get_product_details":
        return get_product_details(context["products"], args["product_name"])

    if tool_name == "get_product_faqs":
        return get_product_faqs(context["faqs"], args["product_name"])

    if tool_name == "get_order_by_id":
        return get_order_by_id(
            context["orders"], args["order_id"], context["customer_id"]
        )

    if tool_name == "can_cancel_order":
        order = get_order_by_id(
            context["orders"], args["order_id"], context["customer_id"]
        )
        return can_cancel_order(order)

    if tool_name == "can_return_order":
        order = get_order_by_id(
            context["orders"], args["order_id"], context["customer_id"]
        )
        return can_return_order(order, context["products"])

    if tool_name == "retrieve_policy_section":
        return retrieve_policy_section(context["policies"], args["query"])

    return {"error": "Unknown tool"}
