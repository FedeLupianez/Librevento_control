<script lang="ts">
	import '../app.css';
	import Header from '../components/Header.svelte';
	import Footer from '../components/Footer.svelte';

	let { children } = $props();
</script>

<div class="app">
	<Header user={null} />
	<main>
		{@render children()}
	</main>
	<Footer />
</div>
