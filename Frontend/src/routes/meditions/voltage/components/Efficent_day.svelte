<script lang="ts">
	import { onMount } from 'svelte';
	export let date: string;
	let day_name = '';
	onMount(() => {
		day_name = new Date(date).toLocaleDateString('es-ES', { weekday: 'long' });
	});
</script>

<div class="relative flex w-full flex-row items-center justify-center gap-2">
	<div class="flex w-1/2 flex-col content-center items-start justify-start">
		<p class="text-2xl">El día mas eficiente de la semana fué el</p>
		<span class="text-4xl font-bold text-[#7A9660]">{day_name}</span>
	</div>
	<img src="/public/images/hojas.svg" alt="Hojita" class="absolute right-0 bottom-0" />
</div>
