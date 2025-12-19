import type { LayoutLoad } from './$types';

let cached: Promise<{ settings: any; apps: any[] }> | null = null;

export const load: LayoutLoad = async ({ fetch }) => {
	if (!cached) {
		cached = Promise.all([
			fetch('http://localhost:8000/settings').then((r) => r.json()),
			fetch('http://localhost:8000/apps').then((r) => r.json())
		]).then(([settings, apps]) => ({ settings, apps }));
	}

	return await cached;
};