from fastapi import FastAPI
from app.utils.loaders import load_products, load_orders, load_faqs

app = FastAPI(title="AI Voice Customer Support")

products = load_products()
orders = load_orders()
faqs = load_faqs()

@app.get("/")
def health():
    return {
        "status": "running",
        "products_loaded": len(products),
        "orders_loaded": len(orders),
        "faqs_loaded": len(faqs)
    }
