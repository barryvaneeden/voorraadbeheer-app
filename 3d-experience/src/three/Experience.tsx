import { Suspense } from 'react';
import { PerspectiveCamera, Sky } from '@react-three/drei';
import { Building } from './Building';
import { SiteEnvironment } from './SiteEnvironment';
import { InteriorDetail } from './InteriorDetail';
import { CameraRig } from './CameraRig';
import { Hotspots } from './Hotspots';
import { LEVELS } from '../data/levels';

export function Experience() {
  return (
    <Suspense fallback={null}>
      <PerspectiveCamera
        makeDefault
        position={LEVELS[0].camera[0].position}
        fov={LEVELS[0].camera[0].fov}
        near={0.5}
        far={600}
      />
      <CameraRig />
      <Hotspots />

      <Sky sunPosition={[80, 40, -40]} turbidity={4} rayleigh={1.2} />
      <hemisphereLight args={['#dfe9f2', '#7fa06c', 0.6]} />
      <directionalLight
        position={[70, 90, 40]}
        intensity={1.4}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-left={-60}
        shadow-camera-right={60}
        shadow-camera-top={60}
        shadow-camera-bottom={-60}
      />
      <fog attach="fog" args={['#cdd8de', 90, 320]} />

      <SiteEnvironment />
      <Building />
      <InteriorDetail />
    </Suspense>
  );
}
