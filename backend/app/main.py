# from fastapi import FastAPI
# from app.utils.loaders import load_products, load_orders, load_faqs

# app = FastAPI(title="AI Voice Customer Support")

# products = load_products()
# orders = load_orders()
# faqs = load_faqs()

# @app.get("/")
# def health():
#     return {
#         "status": "running",
#         "products_loaded": len(products),
#         "orders_loaded": len(orders),
#         "faqs_loaded": len(faqs)
#     }

# from app.tools.product_tools import search_products

# @app.get("/test-products")
# def test_products():
#     results = search_products(
#         products,
#         category="Electronics",
#         max_price=50000,
#         min_rating=4.0
#     )
#     return {
#         "count": len(results),
#         "top_3": results[:3]
#     }


from fastapi import FastAPI
from pydantic import BaseModel
from app.agent.orchestrator import process_message

app = FastAPI()


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    reply = process_message(req.session_id, req.message)
    return {"reply": reply}
