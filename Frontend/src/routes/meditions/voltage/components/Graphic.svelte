<script lang="ts">
	import BarChart from '../../components/BarChart.svelte';
	import Icon from '@iconify/svelte';
	import Efficent_day from './Efficent_day.svelte';
	import { theme } from '../../../../stores/theme';
	import { API_HOST } from '$lib/routes';
	import { onMount } from 'svelte';

	export let filter: string | null = '';
	export let mac_address: string;
	export let show_mobile: boolean = false;
	let is_loading: boolean = false;
	let loading_error: string = '';
	let efficent_date: Measurement = {
		date: '',
		voltage: 0,
		meditions: 0,
		min_voltage: 0,
		max_voltage: 0
	};

	const today = new Date();
	today.setDate(today.getDate() + (7 - today.getDay()));
	const current_date = today.toISOString().split('T')[0];
	let actual_date = current_date;
	let min_limit = new Date(actual_date);
	min_limit.setDate(min_limit.getDate() - min_limit.getDay());
	let min_limit_day = min_limit.toISOString().split('T')[0];
	console.log(min_limit_day, actual_date);

	type Measurement = {
		date: string;
		voltage: number;
		meditions: number;
		min_voltage: number;
		max_voltage: number;
	};

	let data: Measurement[] = [];

	const backgroundColors = (value: number) => {
		if (value >= 5) return $theme === 'dark' ? '#5b6950' : '#7A9660';
		if (value >= 4 && value < 5) return '#ebdaa8';
		if (value < 4) return '#c85d4d';
	};

	const check_data = (data: Array<Measurement> | boolean): boolean => {
		if (!data) {
			is_loading = false;
			loading_error = 'No hay datos en esta semana';
			efficent_date.date = '';
			return false;
		}
		is_loading = false;
		loading_error = '';
		return true;
	};

	async function getData(mac_address: string) {
		let route = `${API_HOST}/medicion/obtener_voltajes?macAddress=${mac_address}&fecha_minima=${min_limit_day}&fecha_maxima=${actual_date}`;
		if (filter) {
			route = route + `&filter=${filter}`;
		}
		const response = await fetch(route, { method: 'GET', credentials: 'include' });
		const result = await response.json();
		if (result.error) {
			is_loading = false;
			loading_error = result.message;
			return false;
		}
		loading_error = '';
		return result.data;
	}

	const getEfficentDay = () => {
		efficent_date = data
			.filter((d) => d.date && d.voltage > 0) // Ignora los objetos vacíos
			.reduce((max, d) => (d.voltage > max.voltage ? d : max), {
				date: '',
				voltage: 0
			} as Measurement);
	};

	async function decrement_week() {
		const temp = new Date(min_limit);
		min_limit.setDate(min_limit.getDate() - 7);
		min_limit_day = min_limit.toISOString().split('T')[0];
		// Hago que la fecha maxima de busqueda sea el domingo pasado
		temp.setDate(temp.getDate() - 1);
		actual_date = temp.toISOString().split('T')[0];

		// Hago que la fecha minima sea el lunes pasado
		is_loading = true;
		const newData = await getData(mac_address);
		if (!check_data(newData)) return;
		data = paddDataToMinimun(newData);
		getEfficentDay();
		is_loading = false;
	}

	async function increment_week() {
		// Incremento el dia minimo
		min_limit.setDate(min_limit.getDate() + 7);
		min_limit_day = min_limit.toISOString().split('T')[0];

		let temp = new Date(actual_date);
		// Hago que sea el domingo siguiente
		temp.setDate(new Date(actual_date).getDate() + 7);
		actual_date = temp.toISOString().split('T')[0];

		is_loading = true;
		const newData = await getData(mac_address);
		if (!check_data(newData)) return;
		data = paddDataToMinimun(newData);
		getEfficentDay();
		is_loading = false;
	}

	const paddDataToMinimun = (data: Measurement[]) => {
		const padded = data;
		while (padded.length < 7) {
			padded.push({ voltage: 0, date: '', meditions: 0, min_voltage: 0, max_voltage: 0 });
		}
		return padded;
	};

	const formatDate = (d: Measurement): string => {
		if (!d.date) return '';
		if (filter == 'day') {
			const day_name = new Date(d.date).toLocaleDateString('es-ES', { weekday: 'long' });
			return day_name;
		}
		return d.date;
	};

	onMount(async () => {
		is_loading = true;
		data = await getData(mac_address).then((data) => data);
		if (!check_data(data)) return;
		console.log(data);
		data = paddDataToMinimun(data);
		getEfficentDay();
		is_loading = false;
	});
</script>

<section
	class={`flex w-full ${show_mobile ? 'flex-col' : 'flex-row'} items-center justify-center gap-8`}
>
	<div class="flex w-full flex-col items-center justify-center gap-5">
		{#if is_loading}
			<h1 class="min-h-52 p-28 text-2xl font-bold {$theme === 'dark' ? 'text-white' : ''}">
				Cargando datos de {mac_address}
			</h1>
		{:else if loading_error}
			<h1 class="min-h-52 p-28 text-2xl font-bold text-[#c85d4d]">{loading_error}</h1>
		{:else}
			<div class="flex w-full flex-col items-start justify-center gap-5">
				<h2 class={$theme === 'dark' ? 'text-white' : ''}>Generador: {mac_address}</h2>
				<BarChart
					prom={data.map((d) => d.voltage)}
					min={data.map((d) => d.min_voltage)}
					max={data.map((d) => d.max_voltage)}
					labels={data.map((d) => formatDate(d))}
					backgroundColorFunction={backgroundColors}
				/>
			</div>
		{/if}

		<div id="buttons-container" class="flex flex-row items-center justify-between gap-5">
			<button
				class="rounded-full {$theme === 'dark' ? 'bg-[#5b6950]' : 'bg-[#7A9660]'} p-2 text-white"
				on:click={decrement_week}
			>
				<Icon icon="maki:arrow" class="rotate-180 transform" />
			</button>
			<button
				class="rounded-full {$theme === 'dark' ? 'bg-[#5b6950]' : 'bg-[#7A9660]'} p-2 text-white"
				on:click={increment_week}
			>
				<Icon icon="maki:arrow" />
			</button>
		</div>
	</div>
	{#if efficent_date.date}
		<div class="flex h-full w-1/2 flex-col items-center justify-between gap-5">
			<Efficent_day date={efficent_date.date} />
			<span class={$theme === 'dark' ? 'text-white' : ''}>Más información</span>
		</div>
	{/if}
</section>
