<script>
	import { user } from '../stores/user';
	import Header from '../components/Header.svelte';
</script>

<svelte:head>
	<title>Recepción</title>
	<meta name="description" content="Página de recepción" />
</svelte:head>

<Header />
<main class="flex min-h-screen flex-col items-center">
	{#if !$user}
		<div class="flex h-100 w-full flex-col items-center justify-center">
			<h1 class="text-5xl font-bold">
				<a href="/login">
					<span class="text-[#7A9660]">Inicia Sesión</span>
				</a>
				o
				<a href="/signup">
					<span class="text-[#7A9660]">Crear una Cuenta</span>
				</a>
			</h1>
		</div>
	{:else}
		<h1 class="text-5xl font-bold">Recepción</h1>
		<button
			on:click={() => {
				window.location.href = '/get_generator';
			}}
			class="w-1/2 rounded-full bg-[#7A9660] p-2 text-white">Obtener Generador</button
		>
	{/if}
</main>
