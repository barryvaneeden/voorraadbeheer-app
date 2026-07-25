import { create } from 'zustand';

export type CameraKeyframe = {
  progress: number;
  position: [number, number, number];
  target: [number, number, number];
  fov?: number;
};

export type Hotspot = {
  id: string;
  position: [number, number, number];
  label: string;
  kind: 'advance' | 'info';
  detail?: string;
  nextLevel?: number;
};

export type LevelData = {
  id: number;
  name: string;
  title: string;
  subtitle: string;
  chapterIndex: string;
  camera: CameraKeyframe[];
  hotspots: Hotspot[];
};

interface ExperienceState {
  hasStarted: boolean;
  currentLevel: number;
  levelProgress: number;
  isSettled: boolean;
  isTransitioning: boolean;
  activeInfo: Hotspot | null;
  start: () => void;
  setLevelProgress: (progress: number) => void;
  setSettled: (settled: boolean) => void;
  beginTransition: () => void;
  advanceToLevel: (level: number) => void;
  openInfo: (hotspot: Hotspot) => void;
  closeInfo: () => void;
}

export const useExperienceStore = create<ExperienceState>((set) => ({
  hasStarted: false,
  currentLevel: 0,
  levelProgress: 0,
  isSettled: false,
  isTransitioning: false,
  activeInfo: null,
  start: () => set({ hasStarted: true }),
  setLevelProgress: (progress) => set({ levelProgress: progress }),
  setSettled: (settled) => set({ isSettled: settled }),
  beginTransition: () => set({ isTransitioning: true, isSettled: false, activeInfo: null }),
  advanceToLevel: (level) =>
    set({ currentLevel: level, isTransitioning: false, levelProgress: 0, isSettled: false }),
  openInfo: (hotspot) => set({ activeInfo: hotspot }),
  closeInfo: () => set({ activeInfo: null }),
}));
