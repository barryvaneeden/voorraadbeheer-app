export function InteriorDetail() {
  return (
    <group position={[-2, 33.2, -1]}>
      <pointLight position={[-1, 3.2, -1]} intensity={22} color="#f3d9a8" distance={9} decay={2} />
      <pointLight position={[3, 2.4, -3]} intensity={10} color="#eef2f6" distance={7} decay={2} />
      <mesh receiveShadow position={[0, 0, 0]}>
        <boxGeometry args={[9, 0.15, 8]} />
        <meshStandardMaterial color="#8a5a34" roughness={0.6} />
      </mesh>
      <mesh position={[-2.5, 0.5, -2]} castShadow>
        <boxGeometry args={[2.2, 0.9, 1]} />
        <meshStandardMaterial color="#2c2c2c" roughness={0.4} metalness={0.3} />
      </mesh>
      <mesh position={[-2.5, 1.0, -2]} castShadow>
        <boxGeometry args={[0.1, 0.1, 0.1]} />
        <meshStandardMaterial color="#c9a24b" metalness={0.8} roughness={0.2} />
      </mesh>
      {/* material swatch cards */}
      <mesh position={[-2.9, 0.6, -0.9]} rotation={[0, 0.3, 0]}>
        <boxGeometry args={[1.2, 1.2, 0.06]} />
        <meshStandardMaterial color="#8a5a34" roughness={0.55} />
      </mesh>
      <mesh position={[-4.4, 2.1, -1.4]} rotation={[0, 0.5, 0]}>
        <boxGeometry args={[1.2, 1.2, 0.06]} />
        <meshStandardMaterial color="#c9a24b" metalness={0.85} roughness={0.25} />
      </mesh>
      <mesh position={[1.5, 0.7, -2.6]}>
        <cylinderGeometry args={[0.35, 0.4, 1, 12]} />
        <meshStandardMaterial color="#4a4d51" roughness={0.5} metalness={0.2} />
      </mesh>
    </group>
  );
}
