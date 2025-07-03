<script>
	import { user } from "../stores/user";
</script>

<svelte:head>
	<title>Recepción</title>
	<meta name="description" content="Página de recepción" />
</svelte:head>

<main class="flex flex-col items-center">

	{#if !$user}
		<div class="w-full h-100 flex flex-col items-center justify-center">
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
	{/if}
</main>