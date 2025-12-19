<script lang="ts">
	import { onDestroy } from 'svelte';
	import { goto } from '$app/navigation';

	let now = new Date();
	const tick = () => (now = new Date());

	const interval = setInterval(tick, 1000);
	onDestroy(() => clearInterval(interval));

	$: timeText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	$: dateText = now.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' });

	let startY: number | null = null;
	let currentY: number | null = null;
	let tracking = false;

	const SWIPE_THRESHOLD_PX = 80;

	function onPointerDown(e: PointerEvent) {
		tracking = true;
		startY = e.clientY;
		currentY = e.clientY;
	}

	async function onPointerUp() {
		if (!tracking || startY == null || currentY == null) return;

		const deltaY = startY - currentY; // positive means moved up
		tracking = false;
		startY = null;
		currentY = null;

		if (deltaY > SWIPE_THRESHOLD_PX) {
			await goto('/home');
		}
	}

	function onPointerMove(e: PointerEvent) {
		if (!tracking) return;
		currentY = e.clientY;
	}
</script>

<main class="min-h-[100dvh] w-full bg-neutral-950 text-white">
	<section
		class="relative min-h-[100dvh] w-full overflow-hidden touch-none"
		onpointerdown={onPointerDown}
		onpointermove={onPointerMove}
		onpointerup={onPointerUp}
		onpointercancel={onPointerUp}
	>
		<div class="absolute inset-0 bg-gradient-to-b from-black/40 via-black/30 to-black/60"></div>

		<div class="relative flex min-h-[100dvh] flex-col justify-between p-6 lg:p-8">
			<header class="flex flex-col items-start gap-1">
				<div class="text-6xl font-semibold tracking-tight tabular-nums">{timeText}</div>
				<div class="text-sm font-medium text-white/80">{dateText}</div>
			</header>

			<footer class="flex flex-col items-center gap-3 pb-2">
				<div class="h-1.5 w-16 rounded-full bg-white/60"></div>
				<div class="text-xs font-medium tracking-wide text-white/70">Swipe up</div>
			</footer>
		</div>
	</section>
</main>