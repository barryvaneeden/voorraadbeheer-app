import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/** Wraps each [data-split] element's text in a masked inner span for line reveals. */
export function splitLines() {
  document.querySelectorAll('[data-split]').forEach((el) => {
    const text = el.textContent;
    el.innerHTML = `<span class="split-inner">${text}</span>`;
  });
}

/** One-shot cinematic intro for the hero, played once the preloader clears. */
export function initHeroIntro() {
  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
  tl.to('#hero .eyebrow', { opacity: 1, y: 0, duration: 0.8 }, 0)
    .to(
      '#hero .display-xl .split-inner',
      { y: '0%', duration: 1.1, stagger: 0.12, ease: 'expo.out' },
      0.15
    )
    .to('#hero .lead', { opacity: 1, y: 0, duration: 0.9 }, 0.55)
    .to('#hero .hero-actions', { opacity: 1, y: 0, duration: 0.8 }, 0.7)
    .to('#hero .scroll-cue', { opacity: 1, y: 0, duration: 0.8 }, 0.9);
}

/** Scroll-triggered reveals for every section below the fold. */
export function initScrollReveals() {
  const lines = gsap.utils.toArray('.reveal-line').filter((el) => !el.closest('#hero'));
  lines.forEach((el) => {
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.9,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        toggleActions: 'play none none reverse',
      },
    });
  });

  document.querySelectorAll('.floating-grid').forEach((grid) => {
    const cards = grid.querySelectorAll('.reveal-card');
    gsap.to(cards, {
      opacity: 1,
      y: 0,
      scale: 1,
      duration: 0.8,
      ease: 'power3.out',
      stagger: 0.12,
      scrollTrigger: {
        trigger: grid,
        start: 'top 85%',
        toggleActions: 'play none none reverse',
      },
    });
  });
}

/** Animates every [data-count] stat up to its target once it enters view. */
export function initCounters() {
  document.querySelectorAll('[data-count]').forEach((el) => {
    const target = parseFloat(el.getAttribute('data-count'));
    const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    const obj = { v: 0 };
    gsap.to(obj, {
      v: target,
      duration: 1.4,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 90%',
        once: true,
      },
      onUpdate: () => {
        el.textContent = obj.v.toFixed(decimals);
      },
    });
  });
}
