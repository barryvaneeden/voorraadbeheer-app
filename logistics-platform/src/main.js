import './style.css';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

import { SceneManager } from './scene/index.js';
import { createTruck } from './scene/truck.js';
import { createWarehouse } from './scene/warehouse.js';
import { createDataCore, updateDataCore } from './scene/particles.js';
import { initScrollScenes } from './animations/scrollScenes.js';
import { splitLines, initHeroIntro, initScrollReveals, initCounters } from './animations/reveals.js';
import { initNav, bindSmoothAnchors } from './ui/nav.js';

gsap.registerPlugin(ScrollTrigger);

function initLenis() {
  const lenis = new Lenis({
    duration: 1.1,
    easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
  return lenis;
}

function buildScene() {
  const canvas = document.getElementById('webgl');
  const sceneManager = new SceneManager(canvas);

  const truck = createTruck();
  const warehouse = createWarehouse();
  const dataCore = createDataCore();

  sceneManager.add(truck.group);
  sceneManager.add(warehouse.group);
  sceneManager.add(dataCore.group);

  sceneManager.onUpdate((delta, elapsed) => {
    truck.wheels.forEach((wheel) => {
      wheel.rotation.x -= delta * 0.6;
    });
    updateDataCore(dataCore, delta, elapsed);
    warehouse.lights.forEach((light, i) => {
      light.intensity = 3 + Math.sin(elapsed * 1.4 + i) * 1.2;
    });
  });

  sceneManager.start();

  return { sceneManager, truck, warehouse, dataCore };
}

function runPreloader(onDone) {
  const fill = document.getElementById('preloader-fill');
  const label = document.getElementById('preloader-label');
  const el = document.getElementById('preloader');
  const progress = { v: 0 };

  gsap
    .timeline({
      onComplete: () => {
        gsap.to(el, {
          autoAlpha: 0,
          duration: 0.8,
          ease: 'power2.out',
          onComplete: () => {
            el.style.display = 'none';
            onDone();
          },
        });
      },
    })
    .to(progress, {
      v: 100,
      duration: 1.2,
      ease: 'power2.inOut',
      onUpdate: () => {
        const val = Math.round(progress.v);
        fill.style.width = `${val}%`;
        label.textContent = `INITIALIZING FLEET SYSTEMS — ${val}%`;
      },
    });
}

function boot() {
  splitLines();

  const { sceneManager, truck, warehouse, dataCore } = buildScene();
  const lenis = initLenis();

  initNav();
  bindSmoothAnchors(lenis);
  initScrollScenes({ sceneManager, truck, warehouse, dataCore });
  initScrollReveals();
  initCounters();

  runPreloader(() => {
    initHeroIntro();
    ScrollTrigger.refresh();
  });
}

boot();
