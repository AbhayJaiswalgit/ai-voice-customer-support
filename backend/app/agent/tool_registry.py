TOOLS = {
    "search_products": {
        "description": "Search products by category, price, and rating",
        "args": ["category", "max_price", "min_rating"]
    },
    "get_product_details": {
        "description": "Get full details of a product by name",
        "args": ["product_name"]
    },
    "get_product_faqs": {
        "description": "Get FAQs for a product",
        "args": ["product_name"]
    },
    "get_order_by_id": {
        "description": "Fetch order details using order ID",
        "args": ["order_id"]
    },
    "can_cancel_order": {
        "description": "Check if an order can be cancelled based on policy",
        "args": ["order_id"]
    },
    "can_return_order": {
        "description": "Check if an order can be returned based on policy",
        "args": ["order_id"]
    },
    "retrieve_policy_section": {
        "description": "Retrieve relevant policy text",
        "args": ["query"]
    }
}
