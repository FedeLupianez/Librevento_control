<script lang="ts">
	import Header from '../components/Header.svelte';
	import Footer from '../components/Footer.svelte';
</script>

<svelte:head>
	<title>Recepción</title>
	<meta name="description" content="Página de recepción" />
</svelte:head>

<section>
	<Header user={{ id:0, name: 'Julián', sex: 'hombre', imageUrl: "https://cdn-icons-png.flaticon.com/512/149/149071.png" }} />
</section>

<style>
	section {
		display: flex;
		padding: 0% 7% 0% 7%;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}


</style>

<Footer />