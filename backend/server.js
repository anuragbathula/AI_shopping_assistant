const http = require('http');
const fs = require('fs');
const path = require('path');
const { replyTo } = require('./chat');
const { createOrder } = require('./data/store');

const frontend = path.join(__dirname, '..', 'frontend');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'application/javascript; charset=utf-8' };

function send(res, code, body, type = 'application/json; charset=utf-8') { res.writeHead(code, { 'Content-Type': type }); res.end(typeof body === 'string' ? body : JSON.stringify(body)); }
function readBody(req) { return new Promise((resolve, reject) => { let data = ''; req.on('data', (chunk) => data += chunk); req.on('end', () => { try { resolve(JSON.parse(data || '{}')); } catch { reject(new Error('Invalid request.')); } }); }); }

http.createServer(async (req, res) => {
  try {
    if (req.method === 'POST' && req.url === '/api/chat') { const body = await readBody(req); return send(res, 200, replyTo(body.message)); }
    if (req.method === 'POST' && req.url === '/api/orders') { const body = await readBody(req); const order = createOrder(body.cartDetails, body.customerInfo); return order ? send(res, 201, order) : send(res, 400, { error: 'Please provide at least one item, your name, and email.' }); }
    if (req.method !== 'GET') return send(res, 404, { error: 'Not found.' });
    const requested = req.url === '/' ? 'index.html' : req.url.replace(/^\//, '');
    const file = path.resolve(frontend, requested);
    if (!file.startsWith(frontend) || !fs.existsSync(file)) return send(res, 404, 'Page not found.', 'text/plain; charset=utf-8');
    return send(res, 200, fs.readFileSync(file), types[path.extname(file)] || 'application/octet-stream');
  } catch (error) { return send(res, 500, { error: 'Something went wrong. Please try again.' }); }
}).listen(process.env.PORT || 3001, () => console.log('Shopping assistant running at http://localhost:3001'));
