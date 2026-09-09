# AI Shopping Assistant

A local, dependency-free Python proof of concept for a conversational shopping assistant. It demonstrates RAG-grounded non-transactional help, explicit tool calling for commerce actions, order tracking, delivery estimates, purchase creation, and friendly empty/error states.
##Created only for POC with samples hardcoded mock data added in tools calls so RAg can run with text terms.

## Project structure

```
backend/
  server.py          # Python HTTP API and static-file host (port 3001)
 ## if you are running you can change port to your own machines default, I picked since my machine has different ports occupied.
  chat.py            # Intent handling and customer-safe tool orchestration
  tools.py           # Mock backend tool interfaces and structured demo data
  retrieval.py       # Local retrieval adapter for support context
frontend/
  index.html         # Accessible chat interface
  app.js             # UI state, requests, loading/error handling
  styles.css         # Responsive visual styles
```

## Start locally

1. Install [Python 3.10+](https://www.python.org/downloads/) if it is not already available. No packages need to be installed.
2. From this folder, run:

   ```powershell
   python -m backend.server
   ```

3. Open [http://localhost:3001](http://localhost:3001).

Alternatively, if npm is installed, `npm start` runs the same Python server.

Try `Show Nike t-shirts`, `Show laptops under $1000`, `Do you have running shoes in size 10?`, `Track order 1234`, or `When will order 5678 arrive?`.

Demo order numbers are `1234`, `5678`, and `9012`. Product and order answers are derived solely from structured mock tool results. Retrieval is used only for matching public support content; if it finds nothing, the assistant says so rather than inventing context. The app does not expose internal implementation details.
