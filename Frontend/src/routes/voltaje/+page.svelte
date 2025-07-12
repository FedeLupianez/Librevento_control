<script lang="ts">
	import BarChart from '../../components/BarChart.svelte';
	import { onMount } from 'svelte';
	import { user } from '../../stores/user';
	import { get } from 'svelte/store';

	type VoltajeData = {
		mac: string;
		data: number[];
	};

	let allVoltajes: VoltajeData[] = [];

	const backgroundColors = (value: number) => {
		if (value >= 8) return '#789262';
		if (value >= 5 && value < 8) return '#ebdaa8';
		if (value < 5) return '#c85d4d';
	};

	async function getMacAddress() {
		const $user = get(user);
		if (!$user) return [];
		const response = await fetch(
			`http://localhost:8000/generador/macAddress?id_usuario=${$user.id_usuario}`,
			{ method: 'GET', credentials: 'include' }
		);
		const data = await response.json();
		return data ?? [];
	}

	onMount(async () => {
		const $user = get(user);
		if (!$user) return;

		const macAddresses = await getMacAddress();
		if (!macAddresses.data || macAddresses.data.length === 0) return;

		// Tomamos solo la data del primer mac para graficar
		allVoltajes = [];
		const promises = macAddresses.data.map(async (mac: string) => {
			const response = await fetch(
				`http://localhost:8000/medicion/obtener_voltajes?macAddress=${mac}`,
				{ method: 'GET', credentials: 'include' }
			);
			const result = await response.json();

			if (result.data && Array.isArray(result.data)) {
				return { mac, data: result.data };
			}
			return null;
		});
		const results = await Promise.all(promises);
		allVoltajes = results.filter(Boolean) as VoltajeData[];
	});
</script>

<h1>Voltaje generado</h1>

{#if allVoltajes.length > 0}
	{#each allVoltajes as { mac, data }}
		<section class="flex flex-col gap-2">
			<h2>Generador: {mac}</h2>
			<BarChart {data} backgroundColorFunction={backgroundColors} />
		</section>
	{/each}
{:else}
	<p>Cargando datos...</p>
{/if}
