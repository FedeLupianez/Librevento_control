<script lang="ts">
	import { onMount } from 'svelte';
	import { theme } from '../stores/theme';

	let show_mobile: boolean = false;
	function updateShow() {
		show_mobile = window.innerWidth < 900;
	}

	onMount(() => {
		updateShow();
		window.addEventListener('resize', updateShow);
	});
</script>

<footer
	class="absolute left-0 w-full {$theme === 'dark'
		? 'bg-[#5b6950]'
		: 'bg-[#7A9660]'} py-10 text-white"
>
	<div class="flex flex-col items-center justify-center space-y-0">
		<p class="text-center text-sm text-gray-800">
			<a
				href="https://www.instagram.com/instituto.manueldefalla"
				target="_blank"
				rel="noopener noreferrer"
				class="text-gray-800 hover:underline"
			>
				@instituto.manueldefalla
			</a>
		</p>

		<!-- Texto principal -->
		<p class="text-[0.8rem]">Proyecto desarrollado por alumnos del Instituto Manuel de Falla.</p>
		<div class="flex {show_mobile ? 'flex-col' : 'flex-row'} gap-5">
			<p class="text-center text-sm text-gray-800">Lupiañez Federico</p>
			<p class="text-center text-sm text-gray-800">Oliva Katerine</p>
			<p class="text-center text-sm text-gray-800">Pelliza Martina</p>
			<p class="text-center text-sm text-gray-800">Secco Eliana</p>
		</div>
	</div>
</footer>
