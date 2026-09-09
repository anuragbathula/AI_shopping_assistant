"""Public, structured interfaces supplied by the commerce backend.

The conversation layer calls only these functions; it has no data-store access.
"""
from datetime import date
from typing import Any
import random

_PRODUCTS = [
    {"id": "p-101", "name": "Nike Club Cotton T-Shirt", "brand": "Nike", "category": "t-shirt", "price": 25.00, "colors": ["Black", "White"], "sizes": ["S", "M", "L", "XL"], "in_stock": True},
    {"id": "p-102", "name": "Nike Sportswear Essential T-Shirt", "brand": "Nike", "category": "t-shirt", "price": 30.00, "colors": ["Blue", "Grey"], "sizes": ["XS", "S", "M", "L"], "in_stock": True},
    {"id": "p-103", "name": "Nike Dri-FIT Training T-Shirt", "brand": "Nike", "category": "t-shirt", "price": 35.00, "colors": ["Black", "Red"], "sizes": ["S", "M", "L"], "in_stock": False},
    {"id": "p-301", "name": "TrailRun 10 Running Shoe", "brand": "TrailRun", "category": "running shoes", "price": 89.00, "colors": ["Blue", "Orange"], "sizes": ["8", "9", "10", "11", "12"], "in_stock": True},
    {"id": "p-401", "name": "Everyday 14-inch Laptop", "brand": "Northstar", "category": "laptop", "price": 799.00, "colors": ["Silver"], "sizes": [], "in_stock": True},
    {"id": "p-402", "name": "Studio 15-inch Laptop", "brand": "Northstar", "category": "laptop", "price": 1199.00, "colors": ["Grey"], "sizes": [], "in_stock": True},
]

_ORDERS = {
    "1234": {"order_id": "1234", "status": "Shipped", "status_date": "September 6, 2026", "tracking": "DEMO-TRACK-1234", "delivery_estimate": "September 10–12, 2026"},
    "5678": {"order_id": "5678", "status": "Processing", "status_date": "September 8, 2026", "delivery_estimate": "September 13–15, 2026"},
    "9012": {"order_id": "9012", "status": "Delivered", "status_date": "September 4, 2026", "tracking": "DEMO-TRACK-9012"},
}


def searchProducts(query: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    filters = filters or {}
    terms = query.casefold().split()
    matches = []
    for product in _PRODUCTS:
        searchable = f"{product['name']} {product['brand']} {product['category']}".casefold()
        if filters.get("brand") and product["brand"].casefold() != str(filters["brand"]).casefold():
            continue
        if filters.get("category") and product["category"].casefold() != str(filters["category"]).casefold():
            continue
        if filters.get("size") and str(filters["size"]) not in product["sizes"]:
            continue
        if filters.get("max_price") is not None and product["price"] > filters["max_price"]:
            continue
        if filters.get("in_stock") and not product["in_stock"]:
            continue
        if terms and not any(term in searchable for term in terms) and not filters:
            continue
        matches.append(product.copy())
    return matches


def getProductDetails(productId: str) -> dict[str, Any] | None:
    return next((product.copy() for product in _PRODUCTS if product["id"] == productId), None)


def getOrderStatus(orderId: str) -> dict[str, Any] | None:
    order = _ORDERS.get(str(orderId))
    return order.copy() if order else None


def getDeliveryEstimate(orderId: str) -> dict[str, Any] | None:
    order = getOrderStatus(orderId)
    if not order:
        return None
    return {"order_id": order["order_id"], "delivery_estimate": order.get("delivery_estimate")}


def createOrder(cartDetails: dict[str, Any], customerInfo: dict[str, Any]) -> dict[str, Any] | None:
    if not cartDetails.get("items") or not customerInfo.get("name") or not customerInfo.get("email"):
        return None
    order_id = str(random.randint(100000, 999999))
    _ORDERS[order_id] = {"order_id": order_id, "status": "Processing", "status_date": date.today().isoformat()}
    return {"order_id": order_id, "status": "Processing", "item_count": len(cartDetails["items"])}
