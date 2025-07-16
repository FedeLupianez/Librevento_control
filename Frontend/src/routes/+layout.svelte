<script lang="ts">
	import '../app.css';
	import Footer from '../components/Footer.svelte';

	let { children } = $props();
</script>

<div class="app">
	<main>
		{@render children()}
	</main>
	<Footer />
</div>
