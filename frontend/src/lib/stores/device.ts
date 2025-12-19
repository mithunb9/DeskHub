import { writable } from 'svelte/store';

export type DeviceSettings = {
	deviceName: string;
	timeFormat: '12h' | '24h';
	theme: 'dark' | 'light';
	wallpaper: 'gradient' | string;
};

export type Apps = {
    name: string;
};

export type DeviceData = {
    settings: DeviceSettings;
    apps: Apps[];
};

export const deviceData = writable<DeviceData | null>(null);