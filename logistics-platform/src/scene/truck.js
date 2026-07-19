import * as THREE from 'three';

const CYAN = 0x6ff3ff;
const AMBER = 0xff9a52;

/**
 * Procedurally built low-poly semi-truck, standing in for a Blender/Spline
 * GLTF export (see README — swap in via GLTFLoader against this same
 * `truck.group` transform without touching the scroll timelines).
 * Returns a solid PBR variant and a glowing wireframe variant, pre-aligned,
 * so the scroll timeline can cross-fade between them.
 */
export function createTruck() {
  const group = new THREE.Group();
  const solidGroup = new THREE.Group();
  const wireGroup = new THREE.Group();
  group.add(solidGroup, wireGroup);

  const wheels = [];

  const bodyMat = new THREE.MeshStandardMaterial({
    color: 0x2a3242,
    metalness: 0.65,
    roughness: 0.35,
  });
  const trimMat = new THREE.MeshStandardMaterial({
    color: 0x4a5568,
    metalness: 0.85,
    roughness: 0.25,
  });
  const glassMat = new THREE.MeshStandardMaterial({
    color: 0x0e2530,
    metalness: 0.2,
    roughness: 0.1,
    emissive: 0x1a4a55,
    emissiveIntensity: 0.4,
  });
  const lightMat = new THREE.MeshStandardMaterial({
    color: CYAN,
    emissive: CYAN,
    emissiveIntensity: 2.2,
  });
  const ambientLightMat = new THREE.MeshStandardMaterial({
    color: AMBER,
    emissive: AMBER,
    emissiveIntensity: 1.8,
  });
  const wheelMat = new THREE.MeshStandardMaterial({
    color: 0x08090c,
    metalness: 0.4,
    roughness: 0.55,
  });
  const hubMat = new THREE.MeshStandardMaterial({
    color: 0x3a4250,
    metalness: 0.95,
    roughness: 0.2,
  });

  const wireMat = new THREE.LineBasicMaterial({
    color: CYAN,
    transparent: true,
    opacity: 0.9,
  });

  /** Adds a mesh to the solid group and a matching edge-line twin to the wire group. */
  function part(geometry, material, position = [0, 0, 0], rotation = [0, 0, 0]) {
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(...position);
    mesh.rotation.set(...rotation);
    solidGroup.add(mesh);

    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geometry), wireMat);
    edges.position.copy(mesh.position);
    edges.rotation.copy(mesh.rotation);
    wireGroup.add(edges);

    return mesh;
  }

  // ---- Cab ----
  part(new THREE.BoxGeometry(2.1, 1.5, 2.0), bodyMat, [2.4, 1.35, 0]);
  part(new THREE.BoxGeometry(2.15, 0.55, 2.05), trimMat, [2.4, 0.5, 0]); // lower skirt
  part(new THREE.BoxGeometry(1.9, 0.7, 1.9), glassMat, [2.75, 2.1, 0]); // windshield block
  part(new THREE.BoxGeometry(0.5, 0.3, 2.2), trimMat, [1.55, 1.85, 0]); // hood
  part(new THREE.BoxGeometry(0.08, 0.4, 2.3), lightMat, [1.3, 1.9, 0]); // grille light strip

  // headlights
  part(new THREE.SphereGeometry(0.11, 12, 12), lightMat, [1.42, 1.35, 0.85]);
  part(new THREE.SphereGeometry(0.11, 12, 12), lightMat, [1.42, 1.35, -0.85]);

  // mirrors
  part(new THREE.BoxGeometry(0.06, 0.32, 0.2), trimMat, [2.9, 1.9, 1.15]);
  part(new THREE.BoxGeometry(0.06, 0.32, 0.2), trimMat, [2.9, 1.9, -1.15]);

  // exhaust stacks
  part(new THREE.CylinderGeometry(0.07, 0.07, 1.6, 10), trimMat, [1.9, 2.6, 1.05]);
  part(new THREE.CylinderGeometry(0.07, 0.07, 1.6, 10), trimMat, [1.9, 2.6, -1.05]);

  // roof light bar
  part(new THREE.BoxGeometry(1.6, 0.08, 0.12), ambientLightMat, [2.4, 2.28, 0]);

  // ---- Chassis rails ----
  part(new THREE.BoxGeometry(9.6, 0.18, 0.14), trimMat, [-1.3, 0.62, 0.75]);
  part(new THREE.BoxGeometry(9.6, 0.18, 0.14), trimMat, [-1.3, 0.62, -0.75]);

  // underglow strip
  part(new THREE.BoxGeometry(9.2, 0.05, 0.05), lightMat, [-1.3, 0.42, 0]);

  // ---- Trailer ----
  part(new THREE.BoxGeometry(6.6, 2.5, 2.3), bodyMat, [-3.0, 1.85, 0]);
  part(new THREE.BoxGeometry(6.65, 0.15, 2.35), trimMat, [-3.0, 0.6, 0]); // trailer skirt
  // trailer panel seams (thin trims for detail)
  for (let i = 0; i < 4; i += 1) {
    part(
      new THREE.BoxGeometry(0.04, 2.4, 2.32),
      trimMat,
      [-0.6 - i * 1.6, 1.85, 0]
    );
  }
  part(new THREE.BoxGeometry(0.1, 2.5, 2.35), lightMat, [-6.25, 1.85, 0]); // rear light bar

  // ---- Wheels ----
  const wheelGeo = new THREE.CylinderGeometry(0.55, 0.55, 0.45, 20);
  const hubGeo = new THREE.CylinderGeometry(0.2, 0.2, 0.47, 12);
  const wheelPositions = [
    [2.55, 0.55, 1.15], [2.55, 0.55, -1.15], // steer axle
    [0.5, 0.55, 1.15], [0.5, 0.55, -1.15], // drive axle
    [-1.6, 0.55, 1.15], [-1.6, 0.55, -1.15], // trailer axle 1
    [-3.2, 0.55, 1.15], [-3.2, 0.55, -1.15], // trailer axle 2
  ];

  wheelPositions.forEach(([x, y, z]) => {
    const wheelGroup = new THREE.Group();
    wheelGroup.position.set(x, y, z);

    const tire = new THREE.Mesh(wheelGeo, wheelMat);
    tire.rotation.z = Math.PI / 2;
    const hub = new THREE.Mesh(hubGeo, hubMat);
    hub.rotation.z = Math.PI / 2;
    wheelGroup.add(tire, hub);
    solidGroup.add(wheelGroup);

    const tireEdges = new THREE.LineSegments(new THREE.EdgesGeometry(wheelGeo), wireMat);
    tireEdges.rotation.z = Math.PI / 2;
    const wireWheelGroup = new THREE.Group();
    wireWheelGroup.position.set(x, y, z);
    wireWheelGroup.add(tireEdges);
    wireGroup.add(wireWheelGroup);

    wheels.push(wheelGroup, wireWheelGroup);
  });

  // Wireframe variant starts hidden/transparent; the scroll timeline crossfades it.
  wireGroup.traverse((child) => {
    if (child.material) {
      child.material = child.material.clone();
      child.material.transparent = true;
      child.material.opacity = 0;
    }
  });
  solidGroup.traverse((child) => {
    if (child.isMesh) {
      child.material = child.material.clone();
      child.material.transparent = true;
    }
  });

  group.position.set(0, -0.2, 0);
  // The body is modeled with its length along local X (cab at +x, trailer
  // trailing to -x). Rotate -90° so the length runs along world Z instead —
  // cab faces the camera and the trailer recedes into depth, keeping the
  // on-screen silhouette narrow instead of spanning the full viewport width.
  group.rotation.y = -Math.PI / 2;

  return { group, solidGroup, wireGroup, wheels };
}
