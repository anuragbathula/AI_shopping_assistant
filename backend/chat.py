"""Customer-safe orchestration of retrieval and explicit commerce tools."""
import re
from typing import Any

from . import retrieval, tools

_INTERNAL = re.compile(r"\b(schema|database|table|column|sql|logs?|architecture|environment|file path|rag pipeline|model configuration)\b", re.I)
_ORDER_ID = re.compile(r"\b\d{4,}\b")


def _product_line(product: dict[str, Any]) -> str:
    availability = "In stock" if product.get("in_stock") else "Currently unavailable"
    details = [f"{product['name']} — ${product['price']:.2f} ({availability})"]
    if product.get("sizes"):
        details.append("Sizes: " + ", ".join(product["sizes"]))
    if product.get("colors"):
        details.append("Colors: " + ", ".join(product["colors"]))
    return "\n".join(details)


def _product_filters(text: str) -> dict[str, Any]:
    lowered = text.casefold()
    filters: dict[str, Any] = {}
    if "nike" in lowered:
        filters["brand"] = "Nike"
    if re.search(r"t[ -]?shirts?|tees?", lowered):
        filters["category"] = "t-shirt"
    elif "laptop" in lowered:
        filters["category"] = "laptop"
    elif re.search(r"running shoes?|shoes?", lowered):
        filters["category"] = "running shoes"
    size = re.search(r"\bsize\s*(\d{1,2}|xs|s|m|l|xl)\b", lowered)
    if size:
        filters["size"] = size.group(1).upper()
    price = re.search(r"(?:under|below|less than)\s*\$?(\d+(?:\.\d{1,2})?)", lowered)
    if price:
        filters["max_price"] = float(price.group(1))
    return filters


def respond(message: str) -> dict[str, str]:
    """Return a customer-facing reply derived solely from retrieval/tool output."""
    text = str(message or "").strip()
    lowered = text.casefold()
    if not text:
        return {"text": "Please tell me what you would like to shop for, or share an order number."}
    if _INTERNAL.search(text):
        return {"text": "I can help with product search, order tracking, or purchases, but internal system details are not accessible."}

    order_id = _ORDER_ID.search(text)
    order_id = order_id.group() if order_id else None
    delivery_request = bool(re.search(r"deliver|arrival|arrive|estimate", lowered))
    order_request = bool(re.search(r"\b(order|track|tracking|status)\b", lowered))
    if delivery_request:
        if not order_id:
            return {"text": "Please share your order number so I can check its delivery estimate."}
        result = tools.getDeliveryEstimate(order_id)  # Explicit tool call.
        if not result:
            return {"text": f"I couldn’t find order {order_id}. Please check the order number or contact support."}
        estimate = result.get("delivery_estimate")
        return {"text": f"Order {result['order_id']} is estimated to arrive {estimate}. Delivery estimates can change." if estimate else f"Order {result['order_id']} does not currently have a delivery estimate."}
    if order_request and order_id:
        result = tools.getOrderStatus(order_id)  # Explicit tool call.
        if not result:
            return {"text": f"I couldn’t find order {order_id}. Please check the order number or contact support."}
        answer = f"Order {result['order_id']} is {result['status']} as of {result['status_date']}."
        if result.get("tracking"):
            answer += f" Tracking: {result['tracking']}."
        if result.get("delivery_estimate"):
            answer += f" Estimated delivery: {result['delivery_estimate']}."
        return {"text": answer}
    if order_request:
        context = retrieval.retrieve(text)
        return {"text": context[0] if context else "Please share your order number and I’ll look up the latest available status."}
    if re.search(r"\b(buy|purchase|place an order|checkout)\b", lowered):
        return {"text": "I can place an order once you provide the item and your name and email. I’ll confirm the order only after the purchase tool returns a result."}

    filters = _product_filters(text)
    product_request = bool(filters) or bool(re.search(r"\b(product|available|show me|find|search|have)\b", lowered))
    if product_request:
        results = tools.searchProducts("", filters) if filters else tools.searchProducts(text, {})  # Explicit tool call.
        if not results:
            return {"text": "I couldn’t find a matching product from the available results. Try a different brand, category, size, or price range."}
        return {"text": f"I found {len(results)} matching product{'s' if len(results) != 1 else ''}:\n\n" + "\n\n".join(_product_line(product) for product in results) + "\n\nWould you like to narrow this by size, color, or price?"}

    context = retrieval.retrieve(text)
    if context:
        return {"text": context[0]}
    return {"text": "I don’t have enough information to answer that. You can try searching for a product, sharing an order number, or asking about a purchase."}
