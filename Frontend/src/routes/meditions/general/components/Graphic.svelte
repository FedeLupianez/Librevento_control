<script lang="ts">
	import StackedBar from '../../components/StackedBar.svelte';
	import { theme } from '$lib/stores/theme';
	import { API_ROUTES } from '$lib/routes';
	import { onMount } from 'svelte';

	type Voltage_measurment = {
		date: string;
		voltage: number;
		meditions: number;
		min_voltage: number;
		max_voltage: number;
	};

	type Consumption_measurment = {
		date: string;
		consumption: number;
		meditions: number;
		min_consumption: number;
		max_consumption: number;
	};

	let is_loading: boolean = false;
	let loading_error: string = '';

	const today = new Date();
	today.setDate(today.getDate() + (7 - today.getDay()));
	const current_date = today.toISOString().split('T')[0];
	let actual_date = current_date;
	let min_limit = new Date(actual_date);
	min_limit.setDate(min_limit.getDate() - min_limit.getDay());
	let min_limit_day = min_limit.toISOString().split('T')[0];

	let voltage_data: Voltage_measurment[] = [];
	let consumption_data: Consumption_measurment[] = [];

	async function get_data(data_type: string) {
		let route =
			data_type === 'voltage'
				? API_ROUTES.MEASUREMENT.ALL_VOLTAGES
				: API_ROUTES.MEASUREMENT.ALL_CONSUMPTIONS;
		route += `?min_date=${min_limit_day}&max_date=${actual_date}`;
		const response = await fetch(route, {
			method: 'GET',
			credentials: 'include'
		});
		if (!response.ok) {
			loading_error = 'Error al cargar los datos';
			return false;
		}
		const data = await response.json();
		if (data.error) {
			loading_error = data.message;
			return false;
		}
		loading_error = '';
		return data.data;
	}

	let voltage_dataset = {
		label: 'Voltajes',
		data: voltage_data.map((d) => d.voltage),
		backgroundColor: $theme === 'light' ? '#FF6384' : '#FF6384'
	};

	let consumption_dataset = {
		label: 'Consumo',
		data: consumption_data.map((d) => d.consumption),
		backgroundColor: $theme === 'light' ? '#FF6384' : '#FF6384'
	};

	onMount(async () => {
		is_loading = true;
		voltage_data = await get_data('voltage').then((data) => data);
		consumption_data = await get_data('consumption').then((data) => data);
		is_loading = false;
	});
</script>

{#if is_loading}
	<h1 class="min-h-52 p-28 text-2xl font-bold {$theme === 'dark' ? 'text-white' : ''}">
		Cargando datos
	</h1>
{:else}
	<StackedBar labels={['Consumo', 'Voltaje']} datasets={[consumption_dataset, voltage_dataset]} />
{/if}
