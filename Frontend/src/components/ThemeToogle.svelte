<script>
	import { theme } from '../stores/theme';
	import Icon from '@iconify/svelte';

	$: currentTheme = $theme;

	const change_theme = () => {
		theme.update((theme) => (theme === 'dark' ? 'light' : 'dark'));
		console.log(currentTheme);
	};
</script>

<button on:click={change_theme} class="fixed right-5 bottom-5 z-10 hover:cursor-pointer">
	<Icon
		icon={currentTheme === 'dark' ? 'ph:sun-bold' : 'ph:moon-bold'}
		class="h-10 w-10 {currentTheme === 'dark' ? 'text-white' : ''}"
	/>
</button>
