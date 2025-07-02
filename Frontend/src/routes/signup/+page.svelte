<script lang="ts">
	import { fetchUser, user } from '../../stores/user';

	let name: string = '';
	let email: string = '';
	let password: string = '';

	const handleSignUp = async () => {
		const imageUrl: string = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&size=128&background=random&color=fff&rounded=true&format=svg`;

		const response = await fetch('http://localhost:8000/user', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				nombre: name,
				email_usuario: email,
				clave: password,
				sexo: 'male',
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
		<!-- Acá se envía la info del usuario -->
		<!-- <form action="/" method="POST" class="flex flex-col gap-5"> -->
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
		<!-- </form> -->
	{:else}
		<p>Ya estás registrado</p>
	{/if}
</div>
