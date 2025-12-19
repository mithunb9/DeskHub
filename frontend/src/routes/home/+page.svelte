<script lang="ts">
	import { deviceData } from '$lib/stores/device';
</script>

{#if $deviceData}
	<div class="text-sm text-white/60">{$deviceData.settings.deviceName}</div>
{/if}
<main class="min-h-[100dvh] w-full overflow-x-hidden bg-neutral-950 text-white">
	<div class="mx-auto flex min-h-[100dvh] max-w-6xl flex-col gap-6 p-6 lg:p-10">
		<header class="flex items-end justify-between">
			<div class="flex flex-col gap-1">
				<h1 class="text-2xl font-semibold tracking-tight">Home</h1>
				<p class="text-sm text-white/70">Sample apps</p>
			</div>

			<a class="text-sm text-white/70 hover:text-white" href="/">Lock</a>
		</header>

		<section class="grid grid-cols-4 gap-4 sm:grid-cols-5 lg:grid-cols-6">
{#each $deviceData?.apps as app}
				<button
					class="group flex flex-col items-center gap-2 rounded-2xl p-3 hover:bg-white/5 active:bg-white/10"
					type="button"
				>
					<div
						class="grid size-16 place-items-center rounded-2xl bg-white/10 text-base font-semibold group-hover:bg-white/15"
					>
						{app.name.slice(0, 1)}
					</div>
					<div class="text-center">
						<div class="text-sm font-medium">{app.name}</div>
					</div>
				</button>
			    {/each}
		</section>
	</div>
</main>