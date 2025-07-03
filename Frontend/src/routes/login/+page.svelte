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

<div class="flex w-full min-h-150 justify-center items-center">
	<div class="flex flex-col h-100 items-between justify-center gap-10 p-15 border-2 rounded-2xl border-[#7A9660]">
		<h1 class="text-2xl font-bold">Inicio de Sesión</h1>
		<input type="text" name="username" placeholder="Usuario" class="text-center" bind:value={name} required />
		<input type="password" name="password" placeholder="Contraseña" class="text-center" bind:value={password} required />
		<button type="submit" class="bg-[#7A9660] text-white rounded-2xl p-2 cursor-pointer hover:bg-[#6b8755]" on:click|preventDefault={login}>Iniciar Sesión</button>

	</div>
</div>
