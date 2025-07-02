<script lang="ts">
	import { user, fetchUser } from '../../stores/user';

	let name: string = '';
	let password: string = '';
	const login = async () => {
		try {
			const response = await fetch('http://localhost:8000/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email_usuario: name, clave: password }),
				credentials: 'include'
			});

			if (response.ok) {
				const data = await response.json();
				user.set(data);
				await fetchUser();
			} else {
				throw new Error('Login failed');
			}
		} catch (error) {
			console.error(error);
		}
	};
</script>

<div class="flex flex-col items-center justify-center">
	<h1 class="text-2xl font-bold">Inicio de Sesión</h1>
	<input type="text" name="username" placeholder="Usuario" bind:value={name} required />
	<input type="password" name="password" placeholder="Contraseña" bind:value={password} required />
	<button type="submit" on:click|preventDefault={login}>Iniciar Sesión</button>
</div>
