import { useExperienceStore } from '../state/store';
import { getLevel } from '../data/levels';

export function ChapterOverlay() {
  const currentLevel = useExperienceStore((s) => s.currentLevel);
  const levelProgress = useExperienceStore((s) => s.levelProgress);
  const isTransitioning = useExperienceStore((s) => s.isTransitioning);
  const hasStarted = useExperienceStore((s) => s.hasStarted);
  const level = getLevel(currentLevel);

  const visible = hasStarted && !isTransitioning && levelProgress < 0.12;

  return (
    <div className={`chapter ${visible ? 'chapter--visible' : ''}`}>
      <div className="chapter__index">{level.chapterIndex}</div>
      <h2 className="chapter__title">{level.title}</h2>
      <p className="chapter__subtitle">{level.subtitle}</p>
    </div>
  );
}
