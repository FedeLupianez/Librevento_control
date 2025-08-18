<script lang="ts">
	import BarChart from '../../components/BarChart.svelte';
	import Icon from '@iconify/svelte';
	import Efficent_day from './Efficent_day.svelte';
	import { API_HOST } from '$lib/routes';
	import { onMount } from 'svelte';

	export let filter: string | null = '';
	export let mac_address: string;
	let is_loading: boolean = false;
	let efficent_date: Measurement = {
		date: '',
		voltage: 0,
		meditions: 0,
		min_voltage: 0,
		max_voltage: 0
	};

	const today = new Date();
	const current_date = today.toISOString().split('T')[0];
	let min_limit = new Date(today);
	min_limit.setDate(min_limit.getDate() - min_limit.getDay());
	let min_limit_day = min_limit.toISOString().split('T')[0];
	let actual_date = current_date;

	type Measurement = {
		date: string;
		voltage: number;
		meditions: number;
		min_voltage: number;
		max_voltage: number;
	};

	let data: Measurement[] = [];

	const backgroundColors = (value: number) => {
		if (value >= 5) return '#789262';
		if (value >= 4 && value < 5) return '#ebdaa8';
		if (value < 4) return '#c85d4d';
	};

	async function getData(mac_address: string) {
		let route = `${API_HOST}/medicion/obtener_voltajes?macAddress=${mac_address}&fecha_minima=${min_limit_day}&fecha_maxima=${actual_date}`;
		if (filter) {
			route = route + `&filter=${filter}`;
		}
		const response = await fetch(route, { method: 'GET', credentials: 'include' });
		const result = await response.json();
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
		let temp = new Date(actual_date);
		// Hago que la fecha maxima de busqueda sea el domingo pasado
		temp.setDate(new Date(actual_date).getDate() - temp.getDay() - 1);
		actual_date = temp.toISOString().split('T')[0];
		// Hago que la fecha minima sea el lunes pasado
		min_limit.setDate(min_limit.getDate() - min_limit.getDay() - 7);
		min_limit_day = min_limit.toISOString().split('T')[0];

		is_loading = true;
		const newData = await getData(mac_address);
		data = paddDataToMinimun(newData);
		getEfficentDay();
		is_loading = false;
	}

	async function increment_week() {
		let temp = new Date(actual_date);
		temp.setDate(new Date(actual_date).getDate() + 7);
		actual_date = temp.toISOString().split('T')[0];
		min_limit.setDate(min_limit.getDate() + 7);
		min_limit_day = min_limit.toISOString().split('T')[0];

		is_loading = true;
		const newData = await getData(mac_address);
		data = paddDataToMinimun(newData);
		getEfficentDay();
		is_loading = false;
	}

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

	onMount(async () => {
		is_loading = true;
		data = await getData(mac_address).then((data) => data);
		data = paddDataToMinimun(data);
		getEfficentDay();
		is_loading = false;
	});
</script>

<section class="flex flex-row items-center justify-between">
	{#if is_loading}
		<div class="flex w-full flex-col items-center justify-center">
			Cargando datos de {mac_address}
		</div>
	{:else}
		<div class="flex flex-col items-center justify-center">
			<div class="flex flex-col items-center justify-center gap-5">
				<h2>Generador: {mac_address}</h2>
				<BarChart
					prom={data.map((d) => d.voltage)}
					min={data.map((d) => d.min_voltage)}
					max={data.map((d) => d.max_voltage)}
					labels={data.map((d) => formatDate(d))}
					backgroundColorFunction={backgroundColors}
				/>
			</div>
			<div id="buttons-container" class="flex flex-row items-center justify-between gap-5">
				<button class="rounded-full bg-[#7A9660] p-2 text-white" on:click={decrement_week}>
					<Icon icon="maki:arrow" class="rotate-180 transform" />
				</button>
				<button class="rounded-full bg-[#7A9660] p-2 text-white" on:click={increment_week}>
					<Icon icon="maki:arrow" />
				</button>
			</div>
		</div>
		{#if efficent_date.date}
			<Efficent_day date={efficent_date.date} />
		{/if}
	{/if}
</section>
