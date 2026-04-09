# Frontend – Code2Concept UI

This folder contains the React + Vite frontend for the Code2Concept video generation experience. It provides a simple interface to enter a topic and preview the generated Manim-based explanation video.

The backend API is expected to run at `http://127.0.0.1:8000` (see [src/api.js](src/api.js)).

---

## Tech Stack

- React 18
- Vite
- ESLint (optional, via [eslint.config.js](eslint.config.js))

---

## Getting Started

From the project root:

```bash
cd frontend
npm install
```

Then start the dev server:

```bash
npm run dev
```

Vite will print the local URL (usually `http://127.0.0.1:5173`).

Make sure the backend (FastAPI + Manim) is already running on `http://127.0.0.1:8000` before generating videos.

---

## Project Structure

```text
frontend/
  index.html
  vite.config.js
  src/
    main.jsx        # React entry
    App.jsx         # Main layout and interaction flow
    api.js          # HTTP client for /generate and /video
    components/
      Loader.jsx
      VideoPlayer.jsx
```

The UI is intentionally minimal: type a topic, press **Generate Video**, and the player will show the most recently rendered video once the backend reports success.
