import type { LevelData } from '../state/store';

export const BUILDING = {
  width: 20,
  depth: 14,
  height: 40,
  floors: 9,
  entrance: { x: 0, z: 8 },
};

export const LEVELS: LevelData[] = [
  {
    id: 0,
    name: 'overzicht',
    chapterIndex: 'I',
    title: 'Het Overzicht',
    subtitle: 'Een gebouw, verankerd in zijn omgeving.',
    camera: [
      { progress: 0, position: [82, 112, 88], target: [0, 8, 0], fov: 48 },
      { progress: 0.5, position: [66, 82, 74], target: [0, 9, 0], fov: 45 },
      { progress: 1, position: [50, 55, 60], target: [0, 10, 0], fov: 42 },
    ],
    hotspots: [
      {
        id: 'overzicht-context',
        kind: 'info',
        label: 'De omgeving',
        detail:
          'Het gebouw staat te midden van laagbouw en groen, met een heldere zichtlijn vanaf de hoofdweg.',
        position: [-28, 6, 20],
      },
      {
        id: 'overzicht-advance',
        kind: 'advance',
        label: 'Ontdek de gevel',
        nextLevel: 1,
        position: [6, 20, 8],
      },
    ],
  },
  {
    id: 1,
    name: 'gevel',
    chapterIndex: 'II',
    title: 'Gevel & Entree',
    subtitle: 'De overgang tussen buiten en binnen.',
    camera: [
      { progress: 0, position: [50, 55, 60], target: [0, 10, 0], fov: 42 },
      { progress: 0.45, position: [20, 24, 34], target: [0, 9, 5], fov: 38 },
      { progress: 1, position: [0, 5, 24], target: [0, 5.5, 7], fov: 32 },
    ],
    hotspots: [
      {
        id: 'gevel-materiaal',
        kind: 'info',
        label: 'Gevelmateriaal',
        detail:
          'Een strak grid van glas en lichte natuursteen, onderbroken door verticale ritmelijnen.',
        position: [-7, 9, 10],
      },
      {
        id: 'gevel-advance',
        kind: 'advance',
        label: 'Ga naar boven — verdiepingen',
        nextLevel: 2,
        position: [0, 6, 8],
      },
    ],
  },
  {
    id: 2,
    name: 'verdiepingen',
    chapterIndex: 'III',
    title: 'Verdiepingen',
    subtitle: 'Laag voor laag, van basis tot top.',
    camera: [
      { progress: 0, position: [0, 5, 24], target: [0, 5.5, 7], fov: 32 },
      { progress: 0.4, position: [12, 20, 19], target: [0, 20, 0], fov: 36 },
      { progress: 1, position: [17, 35, 11], target: [0, 35, 0], fov: 34 },
    ],
    hotspots: [
      {
        id: 'verdieping-plattegrond',
        kind: 'info',
        label: 'Plattegrond',
        detail: 'Elke verdieping herhaalt een efficiënte kern met flexibele vloervelden eromheen.',
        position: [10, 24, 6],
      },
      {
        id: 'verdieping-advance',
        kind: 'advance',
        label: 'Bekijk de ruimtes & materialen',
        nextLevel: 3,
        position: [4, 35, 3],
      },
    ],
  },
  {
    id: 3,
    name: 'ruimtes',
    chapterIndex: 'IV',
    title: 'Ruimtes & Materialisatie',
    subtitle: 'Waar architectuur tastbaar wordt.',
    camera: [
      { progress: 0, position: [17, 35, 11], target: [0, 35, 0], fov: 34 },
      { progress: 0.5, position: [6, 35, 4], target: [-2, 34.5, 0], fov: 32 },
      { progress: 1, position: [1.5, 34.6, 0.5], target: [-4, 34.3, -2], fov: 30 },
    ],
    hotspots: [
      {
        id: 'ruimte-materiaal-1',
        kind: 'info',
        label: 'Eiken vloerdelen',
        detail: 'Warme, natuurlijke afwerking die contrasteert met de koele gevel.',
        position: [-3, 33.6, -1],
      },
      {
        id: 'ruimte-materiaal-2',
        kind: 'info',
        label: 'Geborsteld messing',
        detail: 'Detaillering in de kozijnen en balustrades voegt subtiele glans toe.',
        position: [-5, 35.2, -2.5],
      },
      {
        id: 'ruimte-advance',
        kind: 'advance',
        label: 'Terug naar het overzicht',
        nextLevel: 0,
        position: [-1, 33.4, 1.5],
      },
    ],
  },
];

export const getLevel = (id: number): LevelData => LEVELS[id] ?? LEVELS[0];
