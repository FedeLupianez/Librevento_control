<script lang="ts">
	import '../app.css';
	import Footer from '../components/Footer.svelte';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import ThemeToogle from '../components/ThemeToogle.svelte';

	let { children } = $props();

	onMount(() => {
		const saved_theme = localStorage.getItem('theme') ?? 'light';
		theme.set(saved_theme);

		theme.subscribe((value) => {
			document.documentElement.classList.remove('light', 'dark');
			document.documentElement.classList.add(value);
		});
	});
</script>

<div class="app">
	<main>
		{@render children()}
	</main>
	<ThemeToogle />
	<Footer />
</div>
