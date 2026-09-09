# AI Shopping Assistant

A local, dependency-free proof of concept for a conversational shopping assistant. It supports product discovery, order tracking, delivery estimates, friendly empty/error states, and a purchase endpoint.

## Project structure

```
backend/
  server.js          # HTTP API and static-file host
  chat.js            # Intent handling and customer-safe replies
  data/store.js      # Mock backend tool implementations and demo data
frontend/
  index.html         # Accessible chat interface
  app.js             # UI state, requests, loading/error handling
  styles.css         # Responsive visual styles
```

## Start locally

1. Install [Node.js 18+](https://nodejs.org/) if it is not already available.
2. From this folder, run:

   ```powershell
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000).

Try `Show Nike t-shirts`, `Track order 1234`, or `When will order 5678 arrive?`.

Demo order numbers are `1234`, `5678`, and `9012`. This app uses local mock tool functions; the chat layer uses their public results only and does not expose implementation details.
