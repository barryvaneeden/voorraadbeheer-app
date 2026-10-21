/**
 * Zit-sta: a height-adjustable desk on two T-legs, each a two-stage column on a
 * foot bar, with a control pad on the top. The pointer's height sets the desk's
 * height, between sit and stand, on one spring. At rest the desk stands part
 * way, and the pad is the bright mark; while the pointer is on the page the
 * bright goes to the top's rim. The slider is the travel, in world units.
 *
 * The pattern: a continuous value from the pointer's own screen height, so
 * the hit test never reads the moving geometry.
 */
const {
  Cam, clamp, facing, fit, prism, proj, rings, ringAt, rrect, poly,
  spring, stepS, mk, put, register, pointer, disposer, solid,
} = HL;

const LX = 112, LY = 56, H0 = 43, TRAVEL_MAX = 46, REST = 0.4;
const FOOT = 3.5, LOW = 26, CM = 0.7, Y_STAND = 70, Y_SIT = 250;
const LEGS = [14, 98];

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  const C = Cam(45, 0.5, 1.6);
  const hMax = H0 + TRAVEL_MAX;
  fit(C, [[-12, -14, -4], [124, -14, -4], [-12, 70, -4], [124, 70, -4], [0, 0, hMax], [LX, LY, hMax]], 200, 166);
  const P = proj(C), front = facing(C);
  let trav = value, active = false, drawn = NaN;
  const sp = spring(REST, { eps: 0.002 });

  const g = mk("g", {}, svg);
  const [pr, pi] = rings(-12, -14, 124, 70, 10, 2.2);
  put(solid(g), prism(P, front, pr, pi, -4, 0));

  // Far leg, its rail, near leg, its rail, then the top: back to front.
  const legs = LEGS.map((cx) => {
    const [fr, fi] = rings(cx - 3.6, 2, cx + 3.6, 54, 2.6, 0.9);
    put(solid(g), prism(P, front, fr, fi, 0, FOOT));
    const [lr, li] = rings(cx - 4.2, 23.8, cx + 4.2, 32.2, 1.8, 0.8);
    put(solid(g), prism(P, front, lr, li, FOOT, LOW));
    const [ur, ui] = rings(cx - 3.2, 24.8, cx + 3.2, 31.2, 1.4, 0.7);
    const rail = rings(cx - 3.2, 9, cx + 3.2, 47, 1.4, 0.7);
    return { ur, ui, rail, up: solid(g), rl: solid(g) };
  });
  const top = solid(g);
  const [tr, ti] = rings(0, 0, LX, LY, 4, 1.2);
  const pad = mk("path", { class: "nf hi" }, g);
  const padRing = rrect(80, 45, 95, 50.5, 2.6, 6);

  function draw() {
    const H = H0 + trav * sp.x;
    if (H === drawn) return;
    drawn = H;
    for (const l of legs) {
      put(l.up, prism(P, front, l.ur, l.ui, LOW, H - 3));
      put(l.rl, prism(P, front, l.rail[0], l.rail[1], H - 6.5, H - 3));
    }
    put(top, prism(P, front, tr, ti, H - 3, H));
    top.sil.classList.toggle("hi", active);
    pad.setAttribute("d", poly(ringAt(P, padRing, H)));
    pad.classList.toggle("hi", !active);
    pad.classList.toggle("lo", active);
  }

  const B = register(stage, (dt) => { const m = stepS(sp, dt); draw(); return m; });
  bag.add(B.unregister);

  bag.add(pointer(stage, {
    move: (p) => {
      active = true;
      sp.t = clamp((Y_SIT - p[1]) / (Y_SIT - Y_STAND), 0, 1);
      read.textContent = "h " + Math.round((H0 + trav * sp.t) / CM);
      drawn = NaN;
      B.wake();
    },
    leave: () => {
      active = false;
      sp.t = REST;
      read.textContent = "rest";
      drawn = NaN;
      B.wake();
    },
  }));
  bag.add(() => svg.replaceChildren());

  return { set: (v) => { trav = v; drawn = NaN; B.wake(); }, destroy: bag.dispose };
}

hairline({
  name: "zit-sta",
  means: "A sit-stand desk rises and sinks with the pointer's height, on its two telescoping legs.",
  rules: [1, 3, 5, 9],
  range: [24, 34, 46],
  tour: [[200, 80], [200, 235], [200, 150], null],
  mount,
});
