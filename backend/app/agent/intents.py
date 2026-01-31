import re

def detect_intent(message: str) -> dict:
    msg = message.lower()

    # 🔴 ORDER-LEVEL INTENTS (MOST SPECIFIC FIRST)

    # POLICY QUESTIONS FIRST (WHY / CAN I / IS IT ALLOWED)
    if any(q in msg for q in ["can i", "is it", "allowed", "policy"]) and any(
        k in msg for k in ["cancel", "return", "refund", "delivery"]
    ):
        return {"intent": "POLICY_QUERY"}

    if "cancel" in msg:
        return {"intent": "ORDER_CANCEL"}

    # Return specifically for orders
    if "return" in msg and "order" in msg:
        return {"intent": "ORDER_RETURN"}

    if "order" in msg or "track" in msg:
        return {"intent": "ORDER_TRACK"}

    # 🟡 SMALL TALK
    if any(word in msg for word in ["hi", "hello", "hey"]):
        return {"intent": "SMALL_TALK"}

    # 🟡 PRODUCT FAQ (includes returnable questions about product)
    if any(word in msg for word in ["warranty", "refund", "returnable", "use", "usage", "how"]):
        return {
            "intent": "PRODUCT_FAQ",
            "product_name": extract_product_name(message)
        }

    # 🟡 PRODUCT DETAILS
    if any(word in msg for word in ["tell me about", "details", "information"]):
        return {
            "intent": "PRODUCT_DETAILS",
            "product_name": extract_product_name(message)
        }

    # 🟡 POLICY QUESTIONS
    if "policy" in msg or any(word in msg for word in ["return policy", "refund policy", "delivery policy"]):
        return {"intent": "POLICY_QUERY"}


    # 🟡 PRODUCT SEARCH
    if any(word in msg for word in ["show", "find", "search", "buy"]):
        filters = {}

        if "electronics" in msg:
            filters["category"] = "Electronics"
        elif "clothing" in msg:
            filters["category"] = "Clothing"
        elif "home" in msg:
            filters["category"] = "Home"

        price_match = re.search(r"under\s*(\d+)", msg)
        if price_match:
            filters["max_price"] = int(price_match.group(1))

        if "top rated" in msg or "best rated" in msg:
            filters["min_rating"] = 4.0

        return {
            "intent": "PRODUCT_SEARCH",
            "filters": filters
        }

    return {"intent": "UNKNOWN"}


def extract_product_name(message: str) -> str | None:
    return message
