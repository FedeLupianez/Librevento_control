<script>
	import { page } from '$app/stores';
	import { dev } from '$app/environment';
	import Header from '../components/Header.svelte';
	$: error = $page.error;
	$: status = $page.status;
</script>

<svelte:head>
	<title>Error {status}</title>
</svelte:head>

<Header />
<div class="flex min-h-screen flex-col items-center justify-center">
	{#if status === 404}
		<span class="text-9xl text-[#c85d4d]">404</span>
		<span class="text-3xl font-bold">Estamos Trabajando...</span>
	{:else}
		<span class="text-2xl">Error {status}</span>
		<p>Ha ocurrido un error inesperado</p>
		{#if dev}
			<pre>{error?.message}</pre>
		{/if}
	{/if}
</div>
