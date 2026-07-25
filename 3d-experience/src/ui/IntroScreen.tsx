import { useExperienceStore } from '../state/store';

export function IntroScreen() {
  const hasStarted = useExperienceStore((s) => s.hasStarted);
  const start = useExperienceStore((s) => s.start);

  return (
    <div className={`intro ${hasStarted ? 'intro--hidden' : ''}`}>
      <div className="intro__eyebrow">Een architectuurverhaal</div>
      <h1 className="intro__title">Het Gebouw</h1>
      <p className="intro__subtitle">
        Ontdek één gebouw, laag voor laag — van omgeving tot materiaal.
      </p>
      <button className="intro__button" onClick={start}>
        Begin de ervaring
      </button>
      <div className="intro__hint">scroll om verder te gaan</div>
    </div>
  );
}
