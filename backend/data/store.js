const products = [
  { id: 'p-101', name: 'Nike Club Cotton T-Shirt', brand: 'Nike', category: 't-shirt', price: 25, colors: ['Black', 'White'], sizes: ['S', 'M', 'L', 'XL'], inStock: true },
  { id: 'p-102', name: 'Nike Sportswear Essential T-Shirt', brand: 'Nike', category: 't-shirt', price: 30, colors: ['Blue', 'Grey'], sizes: ['XS', 'S', 'M', 'L'], inStock: true },
  { id: 'p-103', name: 'Nike Dri-FIT Training T-Shirt', brand: 'Nike', category: 't-shirt', price: 35, colors: ['Black', 'Red'], sizes: ['S', 'M', 'L'], inStock: false },
  { id: 'p-201', name: 'Adidas Trefoil T-Shirt', brand: 'Adidas', category: 't-shirt', price: 28, colors: ['White', 'Green'], sizes: ['S', 'M', 'L', 'XL'], inStock: true }
];

const orders = {
  '1234': { orderId: '1234', status: 'Shipped', statusDate: 'September 6, 2026', tracking: 'DEMO-TRACK-1234', deliveryEstimate: 'September 10–12, 2026' },
  '5678': { orderId: '5678', status: 'Processing', statusDate: 'September 8, 2026', tracking: null, deliveryEstimate: 'September 13–15, 2026' },
  '9012': { orderId: '9012', status: 'Delivered', statusDate: 'September 4, 2026', tracking: 'DEMO-TRACK-9012', deliveryEstimate: null }
};

// These functions represent the application's backend integrations. The chat layer
// only reads their returned public fields and never reaches into the data source.
function searchProducts(query = '', filters = {}) {
  const term = query.toLowerCase();
  return products.filter((product) => {
    const searchable = `${product.name} ${product.brand} ${product.category}`.toLowerCase();
    return (!term || searchable.includes(term)) &&
      (!filters.brand || product.brand.toLowerCase() === filters.brand.toLowerCase()) &&
      (!filters.category || product.category.toLowerCase() === filters.category.toLowerCase()) &&
      (!filters.size || product.sizes.includes(filters.size)) &&
      (!filters.inStock || product.inStock);
  });
}

function getProductDetails(productId) {
  return products.find((product) => product.id === productId) || null;
}

function getOrderStatus(orderId) {
  return orders[String(orderId)] || null;
}

function getDeliveryEstimate(orderId) {
  const order = getOrderStatus(orderId);
  return order ? { orderId: order.orderId, deliveryEstimate: order.deliveryEstimate } : null;
}

function createOrder(cartDetails, customerInfo) {
  if (!cartDetails?.items?.length || !customerInfo?.name || !customerInfo?.email) return null;
  const orderId = String(Math.floor(100000 + Math.random() * 900000));
  orders[orderId] = { orderId, status: 'Processing', statusDate: new Date().toLocaleDateString(), tracking: null, deliveryEstimate: 'To be confirmed' };
  return { orderId, status: 'Processing', itemCount: cartDetails.items.length };
}

module.exports = { searchProducts, getProductDetails, getOrderStatus, getDeliveryEstimate, createOrder };
