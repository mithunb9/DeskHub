<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { deviceData } from '$lib/stores/device';

	let { children, data } = $props();

	let lastData: unknown = null;

	$effect(() => {
		if (data && data !== lastData) {
			lastData = data;
			deviceData.set(data);
		}
	});
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}