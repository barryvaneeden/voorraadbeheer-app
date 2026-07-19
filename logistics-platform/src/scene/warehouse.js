import * as THREE from 'three';

const CYAN = 0x6ff3ff;
const AMBER = 0xff9a52;

/**
 * Procedural autonomous-warehouse corridor: glowing grid floor + racking rows
 * receding into fog, standing in for a Blender-exported environment (see README).
 */
export function createWarehouse() {
  const group = new THREE.Group();
  group.position.set(0, -0.2, -6);

  const rackMat = new THREE.MeshStandardMaterial({
    color: 0x161b22,
    metalness: 0.7,
    roughness: 0.4,
  });
  const shelfGlowMat = new THREE.MeshStandardMaterial({
    color: CYAN,
    emissive: CYAN,
    emissiveIntensity: 1.6,
  });
  const podMat = new THREE.MeshStandardMaterial({
    color: 0x2b3038,
    metalness: 0.5,
    roughness: 0.5,
  });

  // Glowing grid floor
  const grid = new THREE.GridHelper(80, 40, 0x6ff3ff, 0x18222c);
  grid.material.transparent = true;
  grid.material.opacity = 0.35;
  grid.position.y = 0;
  group.add(grid);

  // Racking rows on either side, receding in Z
  const rackCount = 7;
  const rowOffsets = [-4.2, 4.2];

  for (const xOffset of rowOffsets) {
    for (let i = 0; i < rackCount; i += 1) {
      const rack = new THREE.Group();
      rack.position.set(xOffset, 0, -i * 4.5 - 2);

      const frame = new THREE.Mesh(new THREE.BoxGeometry(1.4, 4.2, 1.4), rackMat);
      frame.position.y = 2.1;
      rack.add(frame);

      // shelf glow bands
      for (let s = 0; s < 3; s += 1) {
        const band = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.05, 1.5), shelfGlowMat);
        band.position.y = 0.9 + s * 1.3;
        rack.add(band);
      }

      // storage pods (abstract crates)
      for (let p = 0; p < 3; p += 1) {
        const pod = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.6, 0.9), podMat);
        pod.position.set(0, 1.0 + p * 1.3, 0.1);
        rack.add(pod);
      }

      group.add(rack);
    }
  }

  // Corridor accent lights, alternating cyan / amber, fading into distance
  const lights = [];
  for (let i = 0; i < 5; i += 1) {
    const color = i % 2 === 0 ? CYAN : AMBER;
    const light = new THREE.PointLight(color, 4, 12, 2);
    light.position.set(0, 3, -i * 6 - 2);
    group.add(light);
    lights.push(light);
  }

  group.traverse((child) => {
    if (child.isMesh) {
      child.material = child.material.clone();
      child.material.transparent = true;
      child.material.opacity = 0;
    }
  });
  grid.material.userData.baseOpacity = 0.35;

  return { group, lights, grid };
}
