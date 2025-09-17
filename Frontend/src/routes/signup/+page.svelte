<script lang="ts">
	import { fetchUser, user } from '../../stores/user';
	import { API_HOST } from '$lib/routes';

	let name: string = '';
	let email: string = '';
	let password: string = '';

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
		const sexo: Promise<string> = getGender(name);
		console.log(email);

		const response = await fetch(`${API_HOST}/usuario`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				nombre: name,
				email: email,
				clave: password,
				sexo: (await sexo).toString(),
				foto_perfil: imageUrl
			}),
			credentials: 'include'
		});

		if (!response.ok) {
			console.error('Error signing up:', await response.text());
			return;
		}
		await fetchUser();
	};
</script>

<svelte:head>
	<title>Crear Cuenta</title>
	<meta name="description" content="Crear una Cuenta" />
</svelte:head>

<div class="mr-10 flex min-h-screen flex-col items-start">
	<span
		class="
		mt-8
		ml-15
		text-left
		text-[50px]
		font-bold
		text-[#141414]">Crea tu cuenta</span
	>

	{#if !$user}
		<div class="flex min-h-150 flex-col gap-4 pl-15">
			<input
				type="email"
				name="email"
				placeholder="Tu correo electrónico"
				class="
					w-[375px]
					border border-gray-800
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
					border border-gray-800
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
					border border-gray-800
					px-4 py-2
					text-left text-[15px]"
				id="name-input"
				bind:value={name}
				required
			/>

			<button
				type="submit"
				class="
				w-[375px]
					border border-gray-800
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
