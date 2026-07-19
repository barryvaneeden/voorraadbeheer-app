import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const SECTION_IDS = ['fleet', 'network', 'intelligence', 'contact'];

export function initNav() {
  const progressFill = document.getElementById('nav-progress-fill');
  const nav = document.getElementById('site-nav');
  const navLinks = gsap.utils.toArray('.nav-links a');

  ScrollTrigger.create({
    trigger: document.body,
    start: 'top top',
    end: 'bottom bottom',
    onUpdate: (self) => {
      progressFill.style.width = `${self.progress * 100}%`;
    },
  });

  const setActive = (id) => {
    navLinks.forEach((a) => a.classList.toggle('active', a.dataset.nav === id));
  };

  SECTION_IDS.forEach((id) => {
    const section = document.getElementById(id);
    if (!section) return;
    ScrollTrigger.create({
      trigger: section,
      start: 'top center',
      end: 'bottom center',
      onEnter: () => setActive(id),
      onEnterBack: () => setActive(id),
    });
  });

  ScrollTrigger.create({
    trigger: document.body,
    start: '80px top',
    onEnter: () => nav.classList.add('scrolled'),
    onLeaveBack: () => nav.classList.remove('scrolled'),
  });
}

/** Routes in-page anchor clicks through Lenis for a cinematic smooth scroll. */
export function bindSmoothAnchors(lenis) {
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const id = link.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      lenis.scrollTo(target, { duration: 1.2, easing: (t) => 1 - Math.pow(1 - t, 3) });
    });
  });
}
