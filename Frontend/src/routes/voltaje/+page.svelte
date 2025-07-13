<script lang="ts">
	import BarChart from '../../components/BarChart.svelte';
	import { onMount } from 'svelte';
	import { user } from '../../stores/user';
	import { get } from 'svelte/store';

	type Measurement = {
		value: number;
		timestamp: string;
	};

	type GeneratorData = {
		mac: string;
		data: Measurement[];
	};

	let allGenerators: GeneratorData[] = [];

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
		allGenerators = [];
		const promises = macAddresses.data.map(async (mac: string) => {
			const response = await fetch(
				`http://localhost:8000/medicion/obtener_voltajes?macAddress=${mac}`,
				{ method: 'GET', credentials: 'include' }
			);
			const result = await response.json();

			if (result.data && Array.isArray(result.data)) {
				console.log(result.data);
				return { mac, data: result.data };
			}
			return null;
		});
		const results = await Promise.all(promises);
		allGenerators = results.filter(Boolean) as GeneratorData[];
	});

	const paddDataToMinimun = (data: Measurement[]) => {
		const padded = [...data];
		while (padded.length < 7) {
			padded.push({ value: 0, timestamp: '' });
		}
		return padded;
	};
</script>

<h1>Voltaje generado</h1>

{#if allGenerators.length > 0}
	{#each allGenerators as { mac, data }}
		<section class="flex flex-col gap-2">
			<h2>Generador: {mac}</h2>
			<BarChart
				data={paddDataToMinimun(data).map((d) => d.value)}
				labels={paddDataToMinimun(data).map((d) => {
					if (!d.timestamp) return '';
					return new Date(d.timestamp).toLocaleTimeString('es-ES', { weekday: 'short' });
				})}
				backgroundColorFunction={backgroundColors}
			/>
		</section>
	{/each}
{:else}
	<p class="w-full text-center text-2xl">Cargando datos...</p>
{/if}
