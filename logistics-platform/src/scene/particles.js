import * as THREE from 'three';

const CYAN = new THREE.Color(0x6ff3ff);
const AMBER = new THREE.Color(0xff9a52);

/**
 * Abstract "AI core" for the intelligence section: a glowing wireframe
 * icosahedron surrounded by a drifting particle data-field.
 */
export function createDataCore() {
  const group = new THREE.Group();
  group.position.set(0, 1.6, -2);

  // --- particle field ---
  const count = 1400;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const radiusBase = 3.2;

  for (let i = 0; i < count; i += 1) {
    const r = radiusBase + Math.random() * 2.4;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(Math.random() * 2 - 1);

    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.6;
    positions[i * 3 + 2] = r * Math.cos(phi);

    const mix = Math.random();
    const c = CYAN.clone().lerp(AMBER, mix < 0.15 ? mix * 3 : 0);
    colors[i * 3] = c.r;
    colors[i * 3 + 1] = c.g;
    colors[i * 3 + 2] = c.b;
  }

  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const particleMat = new THREE.PointsMaterial({
    size: 0.045,
    vertexColors: true,
    transparent: true,
    opacity: 0,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
  });

  const particles = new THREE.Points(particleGeo, particleMat);
  group.add(particles);

  // --- glowing wireframe core ---
  const coreGeo = new THREE.IcosahedronGeometry(1.3, 1);
  const coreEdges = new THREE.LineSegments(
    new THREE.EdgesGeometry(coreGeo),
    new THREE.LineBasicMaterial({ color: 0x6ff3ff, transparent: true, opacity: 0 })
  );
  const coreFill = new THREE.Mesh(
    coreGeo,
    new THREE.MeshBasicMaterial({
      color: 0x1a4a55,
      transparent: true,
      opacity: 0,
      wireframe: false,
    })
  );
  group.add(coreFill, coreEdges);

  // small inner satellites
  const satellites = [];
  for (let i = 0; i < 6; i += 1) {
    const sat = new THREE.Mesh(
      new THREE.OctahedronGeometry(0.09),
      new THREE.MeshBasicMaterial({ color: 0xff9a52, transparent: true, opacity: 0 })
    );
    const angle = (i / 6) * Math.PI * 2;
    sat.userData.angle = angle;
    sat.userData.radius = 2.1;
    sat.userData.speed = 0.25 + Math.random() * 0.15;
    sat.userData.yOff = Math.sin(angle) * 0.4;
    group.add(sat);
    satellites.push(sat);
  }

  return { group, particles, coreEdges, coreFill, satellites };
}

export function updateDataCore(core, delta, elapsed) {
  core.group.rotation.y += delta * 0.08;
  core.coreEdges.rotation.y -= delta * 0.15;
  core.coreEdges.rotation.x = Math.sin(elapsed * 0.2) * 0.15;
  core.particles.rotation.y += delta * 0.02;

  for (const sat of core.satellites) {
    const a = sat.userData.angle + elapsed * sat.userData.speed;
    sat.position.set(
      Math.cos(a) * sat.userData.radius,
      sat.userData.yOff + Math.sin(elapsed * 0.6 + sat.userData.angle) * 0.2,
      Math.sin(a) * sat.userData.radius
    );
  }
}
