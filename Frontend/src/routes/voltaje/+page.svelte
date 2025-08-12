<script lang="ts">
	import BarChart from '../../components/BarChart.svelte';
	import Header from '../../components/Header.svelte';
	import { onDestroy, onMount } from 'svelte';
	import { user } from '../../stores/user';
	import { page } from '$app/stores';
	import Efficent_day from './components/Efficent_day.svelte';

	let filter: string | null = '';
	const today = new Date();
	const current_date = today.toISOString().split('T')[0];
	let min_limit = new Date(today);
	// Restar los dias que faltan para que siempre empiece en lunes
	min_limit.setDate(min_limit.getDate() - min_limit.getDay());
	let min_limit_day = min_limit.toISOString().split('T')[0];
	let actual_date = current_date;

	$: if ($page.url.searchParams.get('filter')) {
		filter = $page.url.searchParams.get('filter');
	}

	let unsubscribe: () => void;
	let filterUnsubscribe: () => void;

	type Measurement = {
		date: string;
		voltage: number;
		meditions: number;
		min_voltage: number;
		max_voltage: number;
	};

	type GeneratorData = {
		mac: string;
		data: Measurement[];
	};

	let allGenerators: GeneratorData[] = [];

	const backgroundColors = (value: number) => {
		if (value >= 5) return '#789262';
		if (value >= 4 && value < 5) return '#ebdaa8';
		if (value < 4) return '#c85d4d';
	};

	async function getMacAddress(id_user: number) {
		const response = await fetch(
			`http://localhost:8000/generador/macAddress?id_usuario=${id_user}`,
			{ method: 'GET', credentials: 'include' }
		);
		const data = await response.json();
		console.log(data);
		return data ?? [];
	}

	async function getData(user_id: number) {
		const macAddresses = await getMacAddress(user_id);
		if (!macAddresses.data || macAddresses.data.length === 0) return;

		// Tomamos solo la data del primer mac para graficar
		allGenerators = [];
		const promises = macAddresses.data.map(async (mac: string) => {
			let route = `http://localhost:8000/medicion/obtener_voltajes?macAddress=${mac}&fecha_minima=${min_limit_day}&fecha_maxima=${actual_date}`;
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
		console.log(actual_date);
		console.log(seven_days_ago);
		unsubscribe = user.subscribe(async ($user) => {
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
			padded.push({ voltage: 0, date: '', meditions: 0, min_voltage: 0, max_voltage: 0 });
		}
		return padded;
	};

	const formatDate = (d: Measurement): string => {
		if (!d.date) return '';
		if (filter == 'dia') {
			return new Date(d.date).toLocaleDateString('es-ES', {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			});
		}
		return d.date;
	};
</script>

<Header />
<h1>Voltaje generado</h1>

<main class="flex min-h-screen flex-col gap-4 p-5">
	{#if allGenerators.length > 0}
		{#each allGenerators as { mac, data }}
			<section class="flex flex-row gap-2">
				<div class="flex flex-col gap-5">
					<h2>Generador: {mac}</h2>
					<BarChart
						data={paddDataToMinimun(data).map((d) => d.voltage)}
						labels={paddDataToMinimun(data).map((d) => formatDate(d))}
						backgroundColorFunction={backgroundColors}
					/>
				</div>
				<Efficent_day date="2025-08-08" />

			</section>
		{/each}
	{:else if $user}
		<p class="w-full text-center text-2xl">Cargando datos...</p>
	{:else}
		<div class="flex flex-col items-center justify-center">
			<span class="text-2xl text-red-500">No estás logueado</span>
			<button
				on:click={() => {
					window.location.href = '/get_generator';
				}}
				class="w-1/2 rounded-full bg-[#7A9660] p-2 text-white">Obtener Generador</button
			>
		</div>
	{/if}
</main>
