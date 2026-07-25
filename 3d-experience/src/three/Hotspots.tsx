import { Html } from '@react-three/drei';
import { useExperienceStore } from '../state/store';
import { getLevel } from '../data/levels';
import { useAdvanceLevel } from '../hooks/useAdvanceLevel';

export function Hotspots() {
  const currentLevel = useExperienceStore((s) => s.currentLevel);
  const isSettled = useExperienceStore((s) => s.isSettled);
  const isTransitioning = useExperienceStore((s) => s.isTransitioning);
  const openInfo = useExperienceStore((s) => s.openInfo);
  const advance = useAdvanceLevel();
  const level = getLevel(currentLevel);
  const visible = isSettled && !isTransitioning;

  return (
    <>
      {level.hotspots.map((h) => (
        <Html key={h.id} position={h.position} center zIndexRange={[10, 0]}>
          <button
            className={`hotspot hotspot--${h.kind} ${visible ? 'is-visible' : ''}`}
            onClick={() => (h.kind === 'advance' ? advance(h.nextLevel ?? 0) : openInfo(h))}
          >
            <span className="hotspot__dot" />
            <span className="hotspot__label">{h.label}</span>
          </button>
        </Html>
      ))}
    </>
  );
}
