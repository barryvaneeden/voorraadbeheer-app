import { useMemo } from 'react';
import * as THREE from 'three';

function mulberry32(seed: number) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function ContextBuildings() {
  const rand = mulberry32(42);
  const buildings = useMemo(() => {
    const items: { position: [number, number, number]; size: [number, number, number] }[] = [];
    const ringRadii = [46, 68, 92];
    ringRadii.forEach((radius, ringIndex) => {
      const count = 8 + ringIndex * 4;
      for (let i = 0; i < count; i++) {
        const angle = (i / count) * Math.PI * 2 + rand() * 0.4;
        const x = Math.cos(angle) * radius + (rand() - 0.5) * 8;
        const z = Math.sin(angle) * radius + (rand() - 0.5) * 8;
        if (Math.abs(x) < 16 && Math.abs(z) < 16) continue;
        const h = 4 + rand() * (10 - ringIndex * 2);
        items.push({ position: [x, h / 2, z], size: [5 + rand() * 4, h, 5 + rand() * 4] });
      }
    });
    return items;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <group>
      {buildings.map((b, i) => (
        <mesh key={i} position={b.position} receiveShadow castShadow>
          <boxGeometry args={b.size} />
          <meshStandardMaterial color="#c7c3bb" roughness={0.9} />
        </mesh>
      ))}
    </group>
  );
}

function Trees() {
  const rand = mulberry32(7);
  const trees = useMemo(() => {
    const items: [number, number, number][] = [];
    for (let i = 0; i < 90; i++) {
      const angle = rand() * Math.PI * 2;
      const radius = 20 + rand() * 80;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      if (Math.abs(x) < 14 && Math.abs(z) < 12) continue;
      items.push([x, 0, z]);
    }
    return items;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const trunkGeo = useMemo(() => new THREE.CylinderGeometry(0.2, 0.25, 1.6, 6), []);
  const canopyGeo = useMemo(() => new THREE.ConeGeometry(1.4, 3, 7), []);

  return (
    <group>
      {trees.map((pos, i) => (
        <group key={i} position={pos}>
          <mesh position={[0, 0.8, 0]} geometry={trunkGeo} castShadow>
            <meshStandardMaterial color="#6b5842" roughness={1} />
          </mesh>
          <mesh position={[0, 2.6, 0]} geometry={canopyGeo} castShadow>
            <meshStandardMaterial color={i % 3 === 0 ? '#4f7a4a' : '#5c8a56'} roughness={0.9} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function Roads() {
  return (
    <group position={[0, 0.02, 0]}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[14, 220]} />
        <meshStandardMaterial color="#3a3a3d" roughness={1} />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[220, 14]} />
        <meshStandardMaterial color="#3a3a3d" roughness={1} />
      </mesh>
    </group>
  );
}

export function SiteEnvironment() {
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[400, 400]} />
        <meshStandardMaterial color="#7fa06c" roughness={1} />
      </mesh>
      <Roads />
      <ContextBuildings />
      <Trees />
    </group>
  );
}
