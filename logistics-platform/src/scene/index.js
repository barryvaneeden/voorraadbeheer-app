import * as THREE from 'three';

/**
 * Owns the single WebGL renderer/camera/scene used behind every section.
 * Sub-scenes (truck, warehouse, particles) are added as groups and
 * cross-faded / repositioned by the scroll-driven timelines.
 */
export class SceneManager {
  constructor(canvas) {
    this.canvas = canvas;
    this.clock = new THREE.Clock();
    this.updateCallbacks = [];

    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x06070a, 0.05);

    this.camera = new THREE.PerspectiveCamera(
      42,
      window.innerWidth / window.innerHeight,
      0.1,
      200
    );
    this.camera.position.set(0, 1.7, 9);
    this.camera.lookAt(0, 1, 0);

    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance',
    });
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.05;

    this._buildLights();

    window.addEventListener('resize', () => this._onResize());

    this._raf = this._raf.bind(this);
  }

  _buildLights() {
    const hemi = new THREE.HemisphereLight(0x5fd0ff, 0x0a0d14, 1.6);

    const key = new THREE.DirectionalLight(0xf3f6ff, 3.2);
    key.position.set(6, 9, 8);

    const rim = new THREE.DirectionalLight(0x6ff3ff, 3.4);
    rim.position.set(-8, 4, -6);

    // Sits near the camera's usual position so front-facing surfaces
    // (the side the visitor actually looks at) don't read as flat black.
    const fillFront = new THREE.DirectionalLight(0xbfe3ff, 1.8);
    fillFront.position.set(2, 3, 12);

    const fillWarm = new THREE.PointLight(0xff9a52, 6, 30, 2);
    fillWarm.position.set(-3, 1.2, 4);

    this.scene.add(hemi, key, rim, fillFront, fillWarm);
  }

  add(object) {
    this.scene.add(object);
    return object;
  }

  onUpdate(fn) {
    this.updateCallbacks.push(fn);
    return () => {
      this.updateCallbacks = this.updateCallbacks.filter((cb) => cb !== fn);
    };
  }

  _onResize() {
    const { innerWidth, innerHeight } = window;
    this.camera.aspect = innerWidth / innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(innerWidth, innerHeight);
  }

  start() {
    this._raf();
  }

  _raf() {
    requestAnimationFrame(this._raf);
    const delta = this.clock.getDelta();
    const elapsed = this.clock.elapsedTime;
    for (const cb of this.updateCallbacks) cb(delta, elapsed);
    this.renderer.render(this.scene, this.camera);
  }
}
