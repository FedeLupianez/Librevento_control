<script>
	import { user } from '../stores/user';
	import Header from '../components/Header.svelte';
	import { ROUTES } from '$lib/routes';
</script>

<svelte:head>
	<title>Librevento</title>
	<meta name="description" content="Página principal" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<Header />
<main class="flex min-h-screen flex-col items-center">
	{#if !$user}
		<div class="flex h-100 w-full flex-col items-center justify-center">
			<h1 class="text-5xl font-bold">
				<a href={`${ROUTES.USER.LOGIN}`}>
					<span class="text-[#7A9660]">Inicia Sesión</span>
				</a>
				o
				<a href={`${ROUTES.USER.SIGN_UP}`}>
					<span class="text-[#7A9660]">Crear una Cuenta</span>
				</a>
			</h1>
		</div>
	{:else}
		<h1 class="text-5xl font-bold">Recepción</h1>
		<button
			on:click={() => {
				window.location.href = `${ROUTES.GET_GENERATOR}`;
			}}
			class="w-1/2 rounded-full bg-[#7A9660] p-2 text-white">Obtener Generador</button
		>
	{/if}
</main>
