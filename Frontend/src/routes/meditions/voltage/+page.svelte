<script lang="ts">
	import Header from '../../../components/Header.svelte';
	import { onDestroy, onMount } from 'svelte';
	import { user } from '../../../stores/user';
	import { page } from '$app/stores';
	import { API_HOST, ROUTES } from '$lib/routes';
	import { goto } from '$app/navigation';
	import Graphic from './components/Graphic.svelte';

	let filter_to_aply: string | null = 'day';
	let is_loading_macs: boolean = false;

	$: if ($page.url.searchParams.get('filter')) {
		filter_to_aply = $page.url.searchParams.get('filter');
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
				filter_to_aply = $page.url.searchParams.get('filter');
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
<main class=" flex min-h-screen flex-col justify-start gap-3 px-10 py-5">
	<div class="flex flex-row items-start justify-between">
		<span class="px-11 py-5 text-2xl font-bold">¿Cómo estuvo tu aerogenerador esta semana?</span>
		<ul class="pl-5">
			<li class="flex flex-row items-start gap-2">
				<span class="text-3xl leading-none text-[#7A9660]">●</span>
				<span>Eficiente</span>
			</li>

			<li class="flex flex-row items-start gap-2">
				<span class="text-3xl leading-none text-[#ebdaa8]">●</span>
				<span>Medianamente</span>
			</li>

			<li class="flex flex-row items-start gap-2">
				<span class="text-3xl leading-none text-[#c85d4d]">●</span>
				<span>Poco</span>
			</li>
		</ul>
	</div>

	{#if is_loading_macs}
		<p class="w-full text-center text-2xl">Cargando datos...</p>
	{:else if allMacs.length > 0}
		<div class="flex flex-col justify-between gap-15 px-10">
			{#each allMacs as mac}
				<Graphic filter={filter_to_aply} mac_address={mac} />
			{/each}
		</div>
	{:else}
		<div class="flex w-full flex-col items-center justify-center gap-6">
			<span class="text-2xl text-red-500">No estás logueado</span>
			<button
				on:click={() => {
					goto(`${ROUTES.USER.SIGN_UP}`);
				}}
				class="w-1/6 cursor-pointer rounded-full bg-[#7A9660] p-2 text-white hover:bg-[#6b8755]"
				>Registrate</button
			>
			<button
				on:click={() => {
					goto(`${ROUTES.USER.LOGIN}`);
				}}
				class="w-1/6 cursor-pointer rounded-full bg-[#7A9660] p-2 text-white hover:bg-[#6b8755]"
				>Inicia sesion</button
			>
		</div>
	{/if}
</main>
