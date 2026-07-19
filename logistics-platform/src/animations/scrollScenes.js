import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/** Fades every mesh/line/points material inside a group to `value`. */
function setGroupOpacity(root, value) {
  root.traverse((child) => {
    if (child.material) child.material.opacity = value;
  });
}

/**
 * Drives one continuous camera journey through the truck (hero → fleet),
 * the warehouse (network) and the AI data core (intelligence → cta),
 * each leg scrubbed to its own section's scroll range.
 */
export function initScrollScenes({ sceneManager, truck, warehouse, dataCore }) {
  const { camera } = sceneManager;
  const lookAt = { x: 0, y: 1, z: 0 };

  sceneManager.onUpdate(() => {
    camera.lookAt(lookAt.x, lookAt.y, lookAt.z);
  });

  function leg(sectionSelector, { camFrom, camTo, lookFrom, lookTo, onUpdate, initial }) {
    const trigger = document.querySelector(sectionSelector);
    if (!trigger) return;

    const apply = (t) => {
      camera.position.set(
        camFrom[0] + (camTo[0] - camFrom[0]) * t,
        camFrom[1] + (camTo[1] - camFrom[1]) * t,
        camFrom[2] + (camTo[2] - camFrom[2]) * t
      );
      lookAt.x = lookFrom[0] + (lookTo[0] - lookFrom[0]) * t;
      lookAt.y = lookFrom[1] + (lookTo[1] - lookFrom[1]) * t;
      lookAt.z = lookFrom[2] + (lookTo[2] - lookFrom[2]) * t;
      if (onUpdate) onUpdate(t);
    };

    // The very first leg also defines the at-rest, unscrolled state.
    if (initial) apply(0);

    const state = { t: 0 };
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger,
        start: 'top top',
        end: 'bottom top',
        scrub: 0.6,
      },
    });
    tl.to(state, {
      t: 1,
      ease: 'none',
      onUpdate: () => {
        // Every leg's tween renders once at creation/refresh time even for
        // sections far below the current scroll position — skip those so
        // the last-registered leg doesn't hijack the camera on load.
        if (tl.scrollTrigger.progress <= 0) return;
        apply(state.t);
      },
    });
  }

  // ---- HERO: truck materializes from wireframe into solid ----
  // Nose-on, offset right of the text column — cab close to camera, trailer
  // receding into depth, so the silhouette stays narrow instead of spanning
  // the full viewport width.
  leg('#hero', {
    camFrom: [0.2, 2, 12.5],
    camTo: [1, 2.2, 9.5],
    lookFrom: [-2.1, 1.3, 2],
    lookTo: [-1.9, 1.4, 1],
    initial: true,
    onUpdate: (t) => {
      // Wireframe never fully disappears — it settles into a faint glowing
      // outline over the solid body once materialized.
      const wireFloor = 0.16;
      setGroupOpacity(truck.wireGroup, 1 - Math.max(0, t - 0.5) * 2 * (1 - wireFloor));
      setGroupOpacity(truck.solidGroup, Math.min(1, t * 1.6));
    },
  });

  // ---- FLEET: camera pulls back into a 3/4 orbit revealing the full rig ----
  leg('#fleet', {
    camFrom: [1, 2.2, 9.5],
    camTo: [4.6, 1.8, -1.5],
    lookFrom: [-1.9, 1.4, 1],
    lookTo: [0, 1.3, -3],
  });

  // ---- NETWORK: truck dissolves, warehouse corridor flies in ----
  leg('#network', {
    camFrom: [4.6, 1.8, -1.5],
    camTo: [0, 2.2, -6],
    lookFrom: [0, 1.3, -3],
    lookTo: [0, 2, -22],
    onUpdate: (t) => {
      const fadeOut = Math.max(0, 1 - t * 2.2);
      setGroupOpacity(truck.solidGroup, fadeOut);
      setGroupOpacity(truck.wireGroup, 0.16 * fadeOut);
      setGroupOpacity(warehouse.group, Math.min(1, t * 1.8));
    },
  });

  // ---- INTELLIGENCE: warehouse dissolves into the AI data core ----
  leg('#intelligence', {
    camFrom: [0, 2.2, -6],
    camTo: [0, 1.4, 4],
    lookFrom: [0, 2, -22],
    lookTo: [0, 1.6, -2],
    onUpdate: (t) => {
      setGroupOpacity(warehouse.group, Math.max(0, 1 - t * 2));
      setGroupOpacity(dataCore.group, Math.min(1, Math.max(0, t - 0.15) * 1.4));
    },
  });

  // ---- CTA: pull back wide, let the core settle ----
  leg('#contact', {
    camFrom: [0, 1.4, 4],
    camTo: [0, 2.0, 7.5],
    lookFrom: [0, 1.6, -2],
    lookTo: [0, 1.6, -1],
    onUpdate: (t) => {
      setGroupOpacity(dataCore.group, 1 - t * 0.55);
    },
  });
}
