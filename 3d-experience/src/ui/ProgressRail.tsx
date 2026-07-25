import { useExperienceStore } from '../state/store';
import { LEVELS } from '../data/levels';

export function ProgressRail() {
  const currentLevel = useExperienceStore((s) => s.currentLevel);
  const hasStarted = useExperienceStore((s) => s.hasStarted);

  return (
    <div className={`progress-rail ${hasStarted ? 'progress-rail--visible' : ''}`}>
      {LEVELS.map((level) => (
        <div
          key={level.id}
          className={`progress-rail__dot ${level.id === currentLevel ? 'is-active' : ''}`}
          title={level.title}
        />
      ))}
    </div>
  );
}
