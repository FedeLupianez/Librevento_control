<script lang="ts">
	import '../app.css';
	import Footer from '../components/Footer.svelte';
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/user';
	import { theme } from '$lib/stores/theme';
	import ThemeToogle from '../components/ThemeToogle.svelte';

	let { children } = $props();

	onMount(() => {
		const storedUser = localStorage.getItem('user');
		const saved_theme = localStorage.getItem('theme') ?? 'light';
		theme.set(saved_theme);

		theme.subscribe((value) => {
			document.documentElement.classList.remove('light', 'dark');
			document.documentElement.classList.add(value);
		});

		if (storedUser) {
			try {
				user.set(JSON.parse(storedUser));
			} catch (e) {
				console.error('Failed to parse user from localStorage', e);
				localStorage.removeItem('user'); // Clear corrupted data
			}
		}
	});
</script>

<div class="app">
	<main>
		{@render children()}
	</main>
	<ThemeToogle />
	<Footer />
</div>
