import { useMemo } from 'react';
import * as THREE from 'three';
import { BUILDING } from '../data/levels';

const FACADE_COLOR = '#d8d3c7';
const GLASS_COLOR = '#7fa8c9';
const ENTRANCE_COLOR = '#1c1f22';

function useWindowInstances() {
  return useMemo(() => {
    const { width, depth, height, floors } = BUILDING;
    const floorHeight = height / floors;
    const bays = 6;
    const bayWidth = width / bays;
    const matrices: THREE.Matrix4[] = [];
    const dummy = new THREE.Object3D();

    for (let floor = 1; floor < floors; floor++) {
      const y = floor * floorHeight + floorHeight * 0.5;
      for (let bay = 0; bay < bays; bay++) {
        const x = -width / 2 + bayWidth * (bay + 0.5);
        // front face
        dummy.position.set(x, y, depth / 2 + 0.05);
        dummy.rotation.set(0, 0, 0);
        dummy.updateMatrix();
        matrices.push(dummy.matrix.clone());
        // back face
        dummy.position.set(x, y, -depth / 2 - 0.05);
        dummy.rotation.set(0, Math.PI, 0);
        dummy.updateMatrix();
        matrices.push(dummy.matrix.clone());
      }
      const sideBays = 4;
      const sideBayWidth = depth / sideBays;
      for (let bay = 0; bay < sideBays; bay++) {
        const z = -depth / 2 + sideBayWidth * (bay + 0.5);
        dummy.position.set(width / 2 + 0.05, y, z);
        dummy.rotation.set(0, Math.PI / 2, 0);
        dummy.updateMatrix();
        matrices.push(dummy.matrix.clone());
        dummy.position.set(-width / 2 - 0.05, y, z);
        dummy.rotation.set(0, -Math.PI / 2, 0);
        dummy.updateMatrix();
        matrices.push(dummy.matrix.clone());
      }
    }
    return matrices;
  }, []);
}

function WindowGrid() {
  const matrices = useWindowInstances();
  const windowGeo = useMemo(() => new THREE.BoxGeometry(2.6, 2.0, 0.08), []);

  return (
    <instancedMesh
      args={[windowGeo, undefined, matrices.length]}
      ref={(mesh) => {
        if (!mesh) return;
        matrices.forEach((m, i) => mesh.setMatrixAt(i, m));
        mesh.instanceMatrix.needsUpdate = true;
      }}
      castShadow
    >
      <meshStandardMaterial
        color={GLASS_COLOR}
        metalness={0.3}
        roughness={0.15}
        emissive={new THREE.Color('#3c5064')}
        emissiveIntensity={0.15}
      />
    </instancedMesh>
  );
}

function FloorLines() {
  const { width, depth, height, floors } = BUILDING;
  const floorHeight = height / floors;
  const lines = useMemo(() => {
    const points: [number, number, number][][] = [];
    for (let f = 1; f < floors; f++) {
      const y = f * floorHeight;
      points.push([
        [-width / 2, y, depth / 2],
        [width / 2, y, depth / 2],
      ]);
    }
    return points;
  }, [depth, floorHeight, floors, width]);

  return (
    <group>
      {lines.map((pts, i) => (
        <line key={i}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              args={[new Float32Array(pts.flat()), 3]}
            />
          </bufferGeometry>
          <lineBasicMaterial color="#8a8478" transparent opacity={0.35} />
        </line>
      ))}
    </group>
  );
}

function Entrance() {
  const { width, height, floors } = BUILDING;
  void width;
  void height;
  void floors;
  return (
    <group position={[0, 0, BUILDING.depth / 2]}>
      <mesh position={[0, 3.5, 0.4]} castShadow receiveShadow>
        <boxGeometry args={[7, 7, 0.9]} />
        <meshStandardMaterial color={ENTRANCE_COLOR} metalness={0.2} roughness={0.4} />
      </mesh>
      <mesh position={[0, 3.5, 0.9]}>
        <boxGeometry args={[5.6, 5.6, 0.15]} />
        <meshStandardMaterial
          color="#bcd6e8"
          metalness={0.1}
          roughness={0.05}
          transparent
          opacity={0.55}
        />
      </mesh>
      {/* canopy */}
      <mesh position={[0, 7.2, 2.4]} castShadow>
        <boxGeometry args={[9, 0.3, 4.6]} />
        <meshStandardMaterial color="#2b2e31" metalness={0.5} roughness={0.3} />
      </mesh>
    </group>
  );
}

function Roof() {
  const { width, depth, height } = BUILDING;
  return (
    <group position={[0, height, 0]}>
      <mesh position={[0, 0.15, 0]} receiveShadow castShadow>
        <boxGeometry args={[width + 0.4, 0.3, depth + 0.4]} />
        <meshStandardMaterial color="#c9c4b8" />
      </mesh>
      <mesh position={[width / 4, 1.2, -depth / 4]} castShadow>
        <boxGeometry args={[3, 2, 3]} />
        <meshStandardMaterial color="#9a9488" />
      </mesh>
    </group>
  );
}

export function Building() {
  const { width, depth, height } = BUILDING;
  return (
    <group>
      <mesh position={[0, height / 2, 0]} receiveShadow castShadow>
        <boxGeometry args={[width, height, depth]} />
        <meshStandardMaterial
          color={FACADE_COLOR}
          roughness={0.75}
          metalness={0.05}
          side={THREE.DoubleSide}
        />
      </mesh>
      <WindowGrid />
      <FloorLines />
      <Entrance />
      <Roof />
    </group>
  );
}
