<script lang="ts">
	import Header from '../../components/Header.svelte';
	import { user } from '../$lib/stores/user';
	import { API_HOST } from '$lib/routes';

	let city: string = '';
	let street: string = '';
	let house_number: number = 0;
	// Función para capitalizar una palabra
	function capitalize(word: string): string {
		return word.charAt(0).toUpperCase() + word.slice(1);
	}
	// Función para capitalizar un string con más de una palabra
	function capitalizeWords(str: string): string {
		return str
			.split(' ')
			.map((word) => capitalize(word))
			.join(' ');
	}

	const handleFormSubmit = async () => {
		try {
			const response = await fetch(`${API_HOST}/generador`, {
				credentials: 'include',
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					id_usuario: $user?.id_usuario,
					ciudad: capitalizeWords(city),
					calle: capitalizeWords(street),
					numero_vivienda: house_number
				})
			});
			const data = await response.json();
			console.log(data);
			// Cambiar al usuario a una página donde se muestre la info
		} catch (error) {
			console.error(error);
		}
	};
</script>

<Header />
<main class="flex min-h-screen flex-col items-center justify-center gap-5">
	<h1 class="text-center text-5xl font-bold text-[#7A9660]">Obtener Generador</h1>
	<div class="flex w-full flex-col items-center justify-center gap-5">
		<input
			type="text"
			class="
				w-full border-2
				border-black px-4
				py-2 text-left text-[15px] outline-none focus:border-[#7A9660] sm:w-1/2
            lg:w-1/3 xl:w-1/4
         "
			bind:value={city}
			placeholder="Ciudad"
		/>
		<input
			type="text"
			class="
				w-full border-2
				border-black px-4
				py-2 text-left text-[15px] outline-none focus:border-[#7A9660] sm:w-1/2
            lg:w-1/3 xl:w-1/4
         "
			bind:value={street}
			placeholder="Calle"
		/>
		<input
			type="number"
			class="
				w-full border-2
				border-black
				px-4 py-2 text-left text-[15px] outline-none focus:border-[#7A9660]
            sm:w-1/2 lg:w-1/3 xl:w-1/4
         "
			bind:value={house_number}
			placeholder="Número de vivienda"
		/>
		<button
			class="cursor-pointer bg-[#7A9660] text-center text-white sm:w-1/2 lg:w-1/3 xl:w-1/4"
			on:click={handleFormSubmit}>Pedir Generador</button
		>
	</div>
</main>
