import { useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { Experience } from './three/Experience';
import { ScrollController } from './scroll/ScrollController';
import { IntroScreen } from './ui/IntroScreen';
import { ChapterOverlay } from './ui/ChapterOverlay';
import { HotspotPanel } from './ui/HotspotPanel';
import { ProgressRail } from './ui/ProgressRail';
import { useExperienceStore } from './state/store';

function App() {
  const hasStarted = useExperienceStore((s) => s.hasStarted);
  const isTransitioning = useExperienceStore((s) => s.isTransitioning);
  const currentLevel = useExperienceStore((s) => s.currentLevel);

  useEffect(() => {
    document.body.style.overflow = hasStarted ? '' : 'hidden';
  }, [hasStarted]);

  return (
    <div className="app">
      <div className="canvas-stage">
        <Canvas shadows dpr={[1, 1.8]}>
          <Experience />
        </Canvas>
      </div>

      <IntroScreen />
      <ChapterOverlay />
      <HotspotPanel />
      <ProgressRail />

      <div className={`veil ${isTransitioning ? 'veil--visible' : ''}`} />

      <div className="scroll-track" key={currentLevel}>
        <ScrollController />
      </div>
    </div>
  );
}

export default App;
