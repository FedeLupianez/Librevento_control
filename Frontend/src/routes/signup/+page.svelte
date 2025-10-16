<script lang="ts">
	import { user } from '$lib/stores/user';
	import { API_ROUTES } from '$lib/routes';
	import {theme} from '$lib/stores/theme'
	import Icon from '@iconify/svelte';

	let name: string = '';
	let email: string = '';
	let password: string = '';
	let gender: string = '';
	let view_gender_menu: boolean = false;

	const getGender = async (name: string): Promise<string> => {
		try {
			const response = await fetch(`https://api.genderize.io?name=${name}`);
			const data = await response.json();
			return data.gender || 'unknown'; // Retorna 'unknown' si no se puede determinar el género
		} catch (error) {
			console.error('Error al obtener el género:', error);
			return 'unknown';
		}
	};

	const handleSignUp = async () => {
		const imageUrl: string = `https://ui-avatars.com/api/?name=${name.replace(' ', '+')}&size=128&background=random&color=fff&rounded=true&format=svg`;
		// const sexo: Promise<string> = getGender(name);
		console.log(email);
		console.log(gender);

		const response = await fetch(API_ROUTES.USER.CREATE, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				nombre: name,
				email: email,
				clave: password,
				sexo: gender,
				foto_perfil: imageUrl
			}),
			credentials: 'include'
		});

		if (!response.ok) {
			console.error('Error signing up:', await response.text());
			return;
		}
	};
</script>

<svelte:head>
	<title>Crear Cuenta</title>
	<meta name="description" content="Crear una Cuenta" />
</svelte:head>

<div class="mr-10 flex min-h-screen flex-col items-start relative">
	<Icon icon="bx:leaf" class="absolute top-0 -right-20 w-200 h-auto {$theme === 'dark'
		? 'text-[#5b6950]'
		: 'text-[#7A9660]'} z-[-1]"/>
	<span
		class="
		mt-8
		ml-15
		text-left
		text-[50px]
		font-bold
		{$theme == 'dark' ? 'text-[#ffffff]' : 'text-[#141414]'}
		">Crea tu cuenta</span
	>

	{#if !$user}
		<div class="flex min-h-150 flex-col gap-4 pl-15">
			<input
				type="email"
				name="email"
				placeholder="Tu correo electrónico"
				class="
					w-[375px]
					border
					{$theme == 'dark' ? 'text-[#ffffff] border-[#ffffff]' : 'text-[#141414] border-gray-800'}
					px-4 py-2
					text-left text-[15px]"
				bind:value={email}
				required
			/>

			<input
				type="password"
				name="clave"
				placeholder="Crea una contraseña"
				class="
					w-[375px]
					border 
					{$theme == 'dark' ? 'text-[#ffffff] border-[#ffffff]' : 'text-[#141414] border-gray-800'}
					px-4 py-2
					text-left text-[15px]"
				bind:value={password}
				required
			/>

			<input
				type="text"
				name="name"
				placeholder="Nombre de usuario"
				class="
					w-[375px]
					border 
					{$theme == 'dark' ? 'text-[#ffffff] border-[#ffffff]' : 'text-[#141414] border-gray-800'}
					px-4 py-2
					text-left text-[15px]"
				id="name-input"
				bind:value={name}
				required
			/>

			<div class="group relative border justify-start {$theme == 'dark' ? 'border-white' : 'border-gray-800'}">
				<button on:click={() => {
					view_gender_menu = !view_gender_menu;
				}} class="w-full text-start px-4 py-2">
				{#if gender}
					{#if gender == "male"}
						Hombre
					{:else if gender == "female"}
						Mujer
					{:else}
						No Binario
					{/if}
				{:else}
				Género
				{/if}
				</button>

				{#if view_gender_menu}
				<div class="flex items-center justify-start flex-col">
					<button class=" w-full border-r-0 border-l-0 border-t-1 border-b-1 border-gray-800 py-2 px-4 cursor-pointer hover:bg-gray-800 hover:text-white" on:click={() => {gender = 'male'; view_gender_menu=false}}>Hombre</button>
					<button class=" w-full border-r-0 border-l-0 border-b-1 border-gray-800 py-2 px-4 cursor-pointer hover:bg-gray-800 hover:text-white" on:click={() => {gender = 'female'; view_gender_menu=false}}>Mujer</button>
					<button class=" w-full border-r-0 border-l-0 border-b-1 border-gray-800 py-2 px-4 cursor-pointer hover:bg-gray-800 hover:text-white" on:click={() => {gender = 'unknow'; view_gender_menu=false}}>No Binario</button>
				</div>
				{/if}

			</div>



			<button
				type="submit"
				class="
				w-[375px]
					border
					{$theme == 'dark' ? 'text-[#ffffff] border-[#ffffff]' : 'text-[#141414] border-gray-800'}
					px-4 py-2
					text-left text-[15px]"
				id="signup-button"
				on:click|preventDefault={handleSignUp}
			>
				Crear cuenta
			</button>
		</div>
	{:else}
		<div class="flex min-h-screen w-full flex-col">
			<p>Ya estás registrado</p>
		</div>
	{/if}
</div>
