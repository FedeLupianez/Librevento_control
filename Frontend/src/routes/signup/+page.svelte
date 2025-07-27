<script lang="ts">
	import { fetchUser, user } from '../../stores/user';

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

		const response = await fetch('http://localhost:8000/usuario', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				nombre: name,
				email_usuario: email,
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

<div class="mr-10 flex min-h-90 w-full min-w-70 flex-col items-center justify-center gap-5">
	<h1 class="text-5xl font-bold">Crear Cuenta</h1>

	{#if !$user}
		<div class="flex min-h-150 w-full flex-col items-center justify-center gap-4">
			<input
				type="text"
				name="name"
				placeholder="Nombre de usuario"
				class="flex w-full items-center justify-center rounded-2xl border border-gray-500 text-center"
				id="name-input"
				bind:value={name}
				required
			/>

			<input
				type="email"
				name="email"
				placeholder="Correo electrónico"
				class="flex w-full items-center justify-center rounded-2xl border border-gray-500 text-center"
				bind:value={email}
				required
			/>

			<input
				type="password"
				name="clave"
				placeholder="Contraseña"
				class="flex w-full items-center justify-center rounded-2xl border border-gray-500 text-center"
				bind:value={password}
				required
			/>
			<button
				type="submit"
				class="flex items-center justify-center rounded-2xl bg-gray-500 text-center"
				id="signup-button"
				on:click|preventDefault={handleSignUp}
			>
				Crear cuenta
			</button>
		</div>
	{:else}
		<div class="flex min-h-150 w-full flex-col">
			<p>Ya estás registrado</p>
		</div>
	{/if}
</div>
