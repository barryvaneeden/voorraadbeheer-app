# VECTOR — Autonomous Logistics Platform

A cinematic, scroll-driven marketing site for a fictional autonomous logistics
company. Built with Three.js/WebGL, GSAP + ScrollTrigger, and Lenis for a
premium, industrial sci-fi feel (glassmorphism UI, glowing wireframes,
staggered typography, one continuous camera journey through the page).

This is a standalone frontend project, independent of the Streamlit inventory
app in the repository root.

## Stack

- **Three.js** — realtime WebGL scene (truck, warehouse, AI data core)
- **GSAP + ScrollTrigger** — scroll-scrubbed camera moves, section reveals
- **Lenis** — smooth/inertial scrolling
- **Vite** — dev server & build, vanilla JS, no framework

## Getting started

```bash
npm install
npm run dev       # local dev server
npm run build     # production build to dist/
npm run preview   # serve the production build locally
```

## How the scene is structured

One `<canvas>` is fixed behind the whole page (`src/scene/index.js`). As the
visitor scrolls, `src/animations/scrollScenes.js` scrubs the camera and
cross-fades three groups in sequence:

1. **Truck** (`src/scene/truck.js`) — materializes from a glowing wireframe
   into a solid model in the hero, then the camera orbits it in Fleet.
2. **Warehouse** (`src/scene/warehouse.js`) — a glowing-grid corridor the
   camera flies through in Network.
3. **AI data core** (`src/scene/particles.js`) — a particle field + wireframe
   core for Intelligence, which stays visible into the closing CTA.

`src/animations/reveals.js` and `src/ui/nav.js` handle the DOM-side
typography reveals, stat counters, and the floating glass nav.

### Swapping in real 3D assets

The truck and warehouse are procedurally built (boxes/cylinders) as a
placeholder — this environment has no network access to fetch or render a
Blender/Spline export. To swap in a real GLTF:

```js
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('/models/truck.glb', (gltf) => {
  truck.group.add(gltf.scene); // same group the scroll timeline already drives
});
```

Keep the same `group` transform (position/rotation) so the existing camera
keyframes in `scrollScenes.js` don't need to change.
