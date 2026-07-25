import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useExperienceStore } from '../state/store';

gsap.registerPlugin(ScrollTrigger);

const CHAPTER_SCROLL_VH = 280;

export function ScrollController() {
  const spacerRef = useRef<HTMLDivElement | null>(null);
  const currentLevel = useExperienceStore((s) => s.currentLevel);
  const setLevelProgress = useExperienceStore((s) => s.setLevelProgress);
  const hasStarted = useExperienceStore((s) => s.hasStarted);

  useEffect(() => {
    const spacer = spacerRef.current;
    if (!spacer || !hasStarted) return;

    const trigger = ScrollTrigger.create({
      trigger: spacer,
      start: 'top top',
      end: 'bottom bottom',
      scrub: 0.35,
      onUpdate: (self) => setLevelProgress(self.progress),
    });

    ScrollTrigger.refresh();

    return () => {
      trigger.kill();
    };
  }, [currentLevel, hasStarted, setLevelProgress]);

  return <div ref={spacerRef} className="scroll-spacer" style={{ height: `${CHAPTER_SCROLL_VH}vh` }} />;
}
