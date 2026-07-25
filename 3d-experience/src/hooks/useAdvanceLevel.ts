import { useCallback } from 'react';
import { useExperienceStore } from '../state/store';

export function useAdvanceLevel() {
  const beginTransition = useExperienceStore((s) => s.beginTransition);
  const advanceToLevel = useExperienceStore((s) => s.advanceToLevel);

  return useCallback(
    (next: number) => {
      beginTransition();
      window.setTimeout(() => {
        window.scrollTo(0, 0);
        advanceToLevel(next);
      }, 520);
    },
    [beginTransition, advanceToLevel],
  );
}
