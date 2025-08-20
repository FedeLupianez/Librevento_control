<script lang="ts">
	import Header from '../../../components/Header.svelte';
	import { onDestroy, onMount } from 'svelte';
	import { user } from '../../../stores/user';
	import { page } from '$app/stores';
	import { API_HOST } from '$lib/routes';
	import Graphic from './components/Graphic.svelte';

	let filter: string | null = '';
	let is_loading_macs: boolean = false;

	$: if ($page.url.searchParams.get('filter')) {
		filter = $page.url.searchParams.get('filter');
	}

	let unsubscribe: () => void;
	let filterUnsubscribe: () => void;

	let allMacs: string[] = [];

	async function getMacAddress(id_user: number) {
		const response = await fetch(`${API_HOST}/generador/macAddress?id_usuario=${id_user}`, {
			method: 'GET',
			credentials: 'include'
		});
		const data = await response.json();
		return data ?? [];
	}

	async function updateMacs(user_id: number) {
		is_loading_macs = true;
		allMacs = await getMacAddress(user_id).then((res) => res.data);
		is_loading_macs = false;
	}

	onMount(() => {
		unsubscribe = user.subscribe(($user) => {
			if (!$user) return;
			updateMacs($user.id_usuario);
		});
		filterUnsubscribe = page.subscribe(($page) => {
			if ($page.url.searchParams.get('filter')) {
				filter = $page.url.searchParams.get('filter');
				if (!$user) return;
				updateMacs($user.id_usuario);
			}
		});
	});

	onDestroy(() => {
		if (unsubscribe) unsubscribe();
		if (filterUnsubscribe) filterUnsubscribe();
	});
</script>

<Header />
<main class=" flex min-h-screen flex-col gap-3 px-10 py-5 justify-start">
	<span class="text-2xl font-bold px-11 py-5">¿Cómo estuvo tu aerogenerador esta semana?</span>

	{#if is_loading_macs}
		<p class="w-full text-center text-2xl">Cargando datos...</p>
	{:else if allMacs.length > 0}
		<div class="flex flex-col justify-between px-10 gap-15">
			{#each allMacs as mac}
				<Graphic {filter} mac_address={mac} />
			{/each}
		</div>
	{:else}
		<div class="flex min-h-screen flex-col items-center justify-center">
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
