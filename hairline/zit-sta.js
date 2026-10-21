/**
 * Zit-sta: a height-adjustable desk on two T-legs, each a two-stage column on a
 * foot bar, with a control pad, a monitor and a stack of folders on the top.
 * The pointer's height sets the desk's height, between sit and stand, on one
 * spring. The monitor rides the top; each folder has a softer spring of its
 * own and can only lag upwards, so on the way down the stack floats a moment
 * and settles. At rest the desk stands part way, and the pad is the bright
 * mark; while the pointer is on the page the bright goes to the top's rim.
 * The slider is the travel, in world units.
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
const FOLD = [[82, 11, 104, 31], [83.5, 10, 105, 30], [81, 12.5, 103, 32.5], [83, 11, 104.5, 31]], FT = 2.2;
const LAG = [null, { k: 70, c: 13 }, { k: 48, c: 11 }, { k: 32, c: 9 }];

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  const C = Cam(45, 0.5, 1.5);
  const hMax = H0 + TRAVEL_MAX;
  fit(C, [[-12, -14, -4], [124, -14, -4], [-12, 70, -4], [124, 70, -4], [0, 0, hMax + 36], [LX, LY, hMax]], 200, 166);
  const P = proj(C), front = facing(C);
  let trav = value, active = false, drawn = "";
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
  const mon = [rings(40, 12, 60, 26, 2, 0.6), rings(48.5, 17.5, 51.5, 20.5, 1, 0.5), rings(27, 16.5, 73, 20, 1.3, 0.55)].map((r) => ({ r, el: solid(g) }));
  const fol = FOLD.map((f, k) => ({ r: rings(f[0], f[1], f[2], f[3], 1.6, 0.6), el: solid(g), sp: LAG[k] && spring(REST, { eps: 0.002, ...LAG[k] }) }));
  const pad = mk("path", { class: "nf hi" }, g);
  const padRing = rrect(80, 45, 95, 50.5, 2.6, 6);

  function draw() {
    const H = H0 + trav * sp.x;
    const key = H + "|" + fol.map((f) => f.sp ? f.sp.x : 0).join();
    if (key === drawn) return;
    drawn = key;
    for (const l of legs) {
      put(l.up, prism(P, front, l.ur, l.ui, LOW, H - 3));
      put(l.rl, prism(P, front, l.rail[0], l.rail[1], H - 6.5, H - 3));
    }
    put(top, prism(P, front, tr, ti, H - 3, H));
    put(mon[0].el, prism(P, front, ...mon[0].r, H, H + 1.2));
    put(mon[1].el, prism(P, front, ...mon[1].r, H + 1.2, H + 10));
    put(mon[2].el, prism(P, front, ...mon[2].r, H + 9, H + 34));
    fol.forEach((f, k) => {
      const z = H0 + trav * (f.sp ? Math.max(sp.x, f.sp.x) : sp.x) + k * FT;
      put(f.el, prism(P, front, ...f.r, z, z + FT));
    });
    top.sil.classList.toggle("hi", active);
    pad.setAttribute("d", poly(ringAt(P, padRing, H)));
    pad.classList.toggle("hi", !active);
    pad.classList.toggle("lo", active);
  }

  const B = register(stage, (dt) => { let m = stepS(sp, dt);
    for (const f of fol) if (f.sp && stepS(f.sp, dt)) m = true;
    draw();
    return m; });
  bag.add(B.unregister);

  bag.add(pointer(stage, {
    move: (p) => {
      active = true;
      sp.t = clamp((Y_SIT - p[1]) / (Y_SIT - Y_STAND), 0, 1);
      for (const f of fol) if (f.sp) f.sp.t = sp.t;
      read.textContent = "h " + Math.round((H0 + trav * sp.t) / CM);
      drawn = "";
      B.wake();
    },
    leave: () => {
      active = false;
      sp.t = REST;
      for (const f of fol) if (f.sp) f.sp.t = REST;
      read.textContent = "rest";
      drawn = "";
      B.wake();
    },
  }));
  bag.add(() => svg.replaceChildren());

  return { set: (v) => { trav = v; drawn = ""; B.wake(); }, destroy: bag.dispose };
}

hairline({
  name: "zit-sta",
  means: "A sit-stand desk with a monitor and a stack of folders rises and sinks with the pointer's height.",
  rules: [1, 3, 5, 9],
  range: [24, 34, 46],
  tour: [[200, 80], [200, 235], [200, 150], null],
  mount,
});
