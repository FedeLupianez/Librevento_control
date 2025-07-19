<script lang="ts">
	import BarChart from '../../components/BarChart.svelte';
	import Header from '../../components/Header.svelte';
	import { onDestroy, onMount } from 'svelte';
	import { user } from '../../stores/user';
	import { page } from '$app/stores';

	let filter: string | null = '';
	$: if ($page.url.searchParams.get('filter')) {
		filter = $page.url.searchParams.get('filter');
		console.log(filter);
	}

	let unsubscribe: () => void;
	let filterUnsubscribe: () => void;

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

	async function getMacAddress(id_user: number) {
		const response = await fetch(
			`http://localhost:8000/generador/macAddress?id_usuario=${id_user}`,
			{ method: 'GET', credentials: 'include' }
		);
		const data = await response.json();
		return data ?? [];
	}

	async function getData(user_id: number) {
		const macAddresses = await getMacAddress(user_id);
		if (!macAddresses.data || macAddresses.data.length === 0) return;

		// Tomamos solo la data del primer mac para graficar
		allGenerators = [];
		const promises = macAddresses.data.map(async (mac: string) => {
			let route = `http://localhost:8000/medicion/obtener_voltajes?macAddress=${mac}`;
			if (filter) {
				route = route + `&filter=${filter}`;
			}
			const response = await fetch(route, { method: 'GET', credentials: 'include' });
			const result = await response.json();

			if (result.data && Array.isArray(result.data)) {
				console.log(result.data);
				return { mac, data: result.data };
			}
			return null;
		});
		const results = await Promise.all(promises);
		allGenerators = results.filter(Boolean) as GeneratorData[];
	}

	onMount(async () => {
		unsubscribe = user.subscribe(async ($user) => {
			console.log('Usuario : ', $user);
			if (!$user) return;
			getData($user.id_usuario);
		});
		filterUnsubscribe = page.subscribe(async ($page) => {
			if ($page.url.searchParams.get('filter')) {
				filter = $page.url.searchParams.get('filter');
				console.log(filter);
				if (!$user) return;
				getData($user.id_usuario);
			}
		});
	});

	onDestroy(() => {
		if (unsubscribe) unsubscribe();
		if (filterUnsubscribe) filterUnsubscribe();
	});

	const paddDataToMinimun = (data: Measurement[]) => {
		const padded = [...data];
		while (padded.length < 7) {
			padded.push({ value: 0, timestamp: '' });
		}
		return padded;
	};
</script>

<Header />
<h1>Voltaje generado</h1>

<main class="flex flex-col gap-4 p-5">
	{#if allGenerators.length > 0}
		{#each allGenerators as { mac, data }}
			<section class="flex flex-col gap-2">
				<h2>Generador: {mac}</h2>
				<BarChart
					data={paddDataToMinimun(data).map((d) => d.value)}
					labels={paddDataToMinimun(data).map((d) => {
						if (!d.timestamp) return '';
						return new Date(d.timestamp).toLocaleDateString('es-ES', {
							year: 'numeric',
							month: 'long',
							day: 'numeric'
						});
					})}
					backgroundColorFunction={backgroundColors}
				/>
			</section>
		{/each}
	{:else}
		<p class="w-full text-center text-2xl">Cargando datos...</p>
	{/if}
</main>
