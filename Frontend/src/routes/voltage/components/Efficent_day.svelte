<script lang="ts">
	export let date: string;
	let day_name = new Date(date).toLocaleDateString('es-ES', { weekday: 'long' });
</script>

<div class="flex flex-row items-center justify-center gap-2">
	<div class="flex flex-col items-center justify-start">
		<p>El día mas eficiente de la semana fué el</p>
		<span class="text-4xl font-bold text-[#7A9660]">{day_name}</span>
	</div>
	<img src="/public/images/hojas.svg" alt="Hojita" />
</div>
