import { useEffect, useMemo, useRef } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { useExperienceStore } from '../state/store';
import { getLevel } from '../data/levels';

function easeSettle(t: number) {
  const c = Math.min(Math.max(t, 0), 1);
  return 1 - Math.pow(1 - c, 3);
}

export function CameraRig() {
  const { camera } = useThree();
  const currentLevel = useExperienceStore((s) => s.currentLevel);
  const levelProgress = useExperienceStore((s) => s.levelProgress);
  const setSettled = useExperienceStore((s) => s.setSettled);
  const isTransitioning = useExperienceStore((s) => s.isTransitioning);

  const level = getLevel(currentLevel);

  const curves = useMemo(() => {
    const [a, b, c] = level.camera;
    const posCurve = new THREE.QuadraticBezierCurve3(
      new THREE.Vector3(...a.position),
      new THREE.Vector3(...b.position),
      new THREE.Vector3(...c.position),
    );
    const targetCurve = new THREE.QuadraticBezierCurve3(
      new THREE.Vector3(...a.target),
      new THREE.Vector3(...b.target),
      new THREE.Vector3(...c.target),
    );
    return { posCurve, targetCurve, fovA: a.fov ?? 40, fovC: c.fov ?? 40 };
  }, [level]);

  const currentLookAt = useRef(new THREE.Vector3(...level.camera[0].target));
  const wasSettled = useRef(false);

  useEffect(() => {
    currentLookAt.current.set(...level.camera[0].target);
    camera.position.set(...level.camera[0].position);
  }, [level, camera]);

  useFrame((_, delta) => {
    if (isTransitioning) return;
    const t = easeSettle(levelProgress);
    const pos = curves.posCurve.getPoint(t);
    const look = curves.targetCurve.getPoint(t);

    const damp = 1 - Math.pow(0.001, delta);
    camera.position.lerp(pos, damp);
    currentLookAt.current.lerp(look, damp);
    camera.lookAt(currentLookAt.current);

    const perspCam = camera as THREE.PerspectiveCamera;
    if (perspCam.isPerspectiveCamera) {
      const fov = THREE.MathUtils.lerp(curves.fovA, curves.fovC, t);
      if (Math.abs(perspCam.fov - fov) > 0.01) {
        perspCam.fov = fov;
        perspCam.updateProjectionMatrix();
      }
    }

    const nowSettled = levelProgress > 0.98;
    if (nowSettled !== wasSettled.current) {
      wasSettled.current = nowSettled;
      setSettled(nowSettled);
    }
  });

  return null;
}
