# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.



## Vite proxy for dev
We use Vite's dev proxy to forward every request beginning with /api to the Django server.

The frontend calls relative URLs like /api/me/, and the browser resolves them against the Vite origin (localhost:5173) and never learns Django is on port 8000. Vite receives the request, forwards it to Django, and returns the response as its own.

Because the browser only ever sees one origin, there's no cross-origin request and the session cookie is sent automatically on every call. Without the proxy we'd need CORS headers in Django, credentials: "include" on every fetch, and SESSION_COOKIE_SAMESITE tuning, all to work around a problem the proxy avoids entirely.

In production the proxy disappears; nginx or Django serves the built React files at / and routes /api to Django. Same single-origin shape, so the frontend code doesn't change.