const chat = document.querySelector('#chat');
const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const status = document.querySelector('#status');

function addMessage(text, role) { const item = document.createElement('article'); item.className = `message ${role}`; item.textContent = text; chat.append(item); chat.scrollTop = chat.scrollHeight; return item; }
async function ask(message) {
  addMessage(message, 'customer'); input.value = ''; input.disabled = true;
  status.textContent = /order\s+\d+/i.test(message) ? 'Looking up your order…' : 'Let me check that for you…';
  try {
    const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    addMessage(data.text, 'assistant');
  } catch (error) { addMessage('Sorry, I couldn’t complete that request. Please try again.', 'assistant error'); }
  finally { input.disabled = false; status.textContent = ''; input.focus(); }
}
form.addEventListener('submit', (event) => { event.preventDefault(); ask(input.value.trim()); });
document.querySelectorAll('.suggestions button').forEach((button) => button.addEventListener('click', () => ask(button.textContent)));
