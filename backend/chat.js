const tools = require('./data/store');

const orderIdFrom = (text) => text.match(/\b\d{4,}\b/)?.[0];
const productCard = (product) => `${product.name} — $${product.price} (${product.inStock ? 'In stock' : 'Currently unavailable'})\nSizes: ${product.sizes.join(', ')} · Colors: ${product.colors.join(', ')}`;

function replyTo(message) {
  const text = String(message || '').trim();
  const lower = text.toLowerCase();
  if (!text) return { text: 'Please tell me what you would like to shop for, or share an order number.' };

  if (/schema|database|table|column|sql|server log|environment/.test(lower)) {
    return { text: 'That internal information is not available. I can help you search products, check an order, or place a purchase.' };
  }

  const orderId = orderIdFrom(text);
  if (/(deliver|arrival|when.*(order|arrive)|estimate)/.test(lower)) {
    if (!orderId) return { text: 'Please share your order number so I can check its delivery estimate.' };
    const estimate = tools.getDeliveryEstimate(orderId);
    if (!estimate) return { text: `I couldn’t find order ${orderId}. Please check the order number or contact support.` };
    return { text: estimate.deliveryEstimate ? `Order ${orderId} is estimated to arrive ${estimate.deliveryEstimate}. Delivery dates can change.` : `Order ${orderId} does not currently have a delivery estimate.` };
  }
  if (/(order.*status|status.*order|track|where.*order)/.test(lower)) {
    if (!orderId) return { text: 'Please share your order number and I’ll look up its status.' };
    const order = tools.getOrderStatus(orderId);
    if (!order) return { text: `I couldn’t find order ${orderId}. Please check the order number or contact support.` };
    const tracking = order.tracking ? ` Tracking: ${order.tracking}.` : '';
    const estimate = order.deliveryEstimate ? ` Estimated delivery: ${order.deliveryEstimate}.` : '';
    return { text: `Order ${order.orderId} is ${order.status} as of ${order.statusDate}.${tracking}${estimate}` };
  }
  if (/(how.*track|track.*order)/.test(lower)) return { text: 'Send me your order number and I can check the latest available status and delivery estimate.' };

  const filters = {};
  if (lower.includes('nike')) filters.brand = 'Nike';
  if (/(t[ -]?shirt|tee)/.test(lower)) filters.category = 't-shirt';
  const size = lower.match(/\b(xs|s|m|l|xl)\b/i)?.[1];
  if (size) filters.size = size.toUpperCase();
  const results = tools.searchProducts(text, filters);
  // Search by filters if the customer's full wording is more specific than catalogue names.
  // If a recognised filter is present, use it even when the rest of the wording
  // is not a literal catalogue name. Otherwise, retain the customer's query.
  const matching = results.length ? results : (Object.keys(filters).length ? tools.searchProducts('', filters) : []);
  if (matching.length) {
    return { text: `I found ${matching.length} matching product${matching.length === 1 ? '' : 's'}:\n\n${matching.map(productCard).join('\n\n')}\n\nWould you like to narrow this by size, color, or price?`, products: matching };
  }
  return { text: 'I couldn’t find a matching product. Try a brand, category, size, or price preference.' };
}

module.exports = { replyTo };
