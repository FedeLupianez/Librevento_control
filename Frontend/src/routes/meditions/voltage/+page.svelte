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
	let mediaQueryList: MediaQueryList;
	let showMobile: boolean = false;

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
			if (!$user) {
				is_loading_macs = false;
				return;
			}
			updateMacs($user.id_usuario);
			mediaQueryList = window.matchMedia('(max-width: 750px)');
			showMobile = mediaQueryList.matches;
			console.log(showMobile);
			mediaQueryList.addEventListener('change', (event) => {
				showMobile = event.matches;
				console.log(showMobile);
			});
			return () => {
				mediaQueryList.removeEventListener('change', (event) => {});
			};
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

<svelte:head>
	<title>Mediciones</title>
	<meta name="description" content="Mediciones" />
</svelte:head>

<Header />
<main
	class={`flex min-h-screen w-full flex-col justify-start gap-3 ${showMobile ? '' : 'px-20'} py-5`}
>
	<div class={`flex flex-row items-start ${showMobile ? 'justify-center' : 'justify-between'}`}>
		<span class="text-2xl font-bold">¿Cómo estuvo tu aerogenerador esta semana?</span>
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
		<div class="flex min-h-[400px] w-full items-center justify-center">
			<p class="w-full text-center text-2xl">Cargando datos...</p>
		</div>
	{:else if allMacs.length > 0}
		<div class="flex flex-col gap-15">
			{#each allMacs as mac}
				<Graphic filter={filter_to_aply} mac_address={mac} show_mobile={showMobile} />
			{/each}
		</div>
	{:else}
		<div class="flex min-h-[400px] w-full flex-col items-center justify-center gap-6">
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
