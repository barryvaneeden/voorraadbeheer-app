import { useExperienceStore } from '../state/store';

export function HotspotPanel() {
  const activeInfo = useExperienceStore((s) => s.activeInfo);
  const closeInfo = useExperienceStore((s) => s.closeInfo);

  return (
    <div className={`info-panel ${activeInfo ? 'info-panel--visible' : ''}`}>
      {activeInfo && (
        <>
          <div className="info-panel__label">{activeInfo.label}</div>
          <p className="info-panel__detail">{activeInfo.detail}</p>
          <button className="info-panel__close" onClick={closeInfo} aria-label="Sluiten">
            ×
          </button>
        </>
      )}
    </div>
  );
}
