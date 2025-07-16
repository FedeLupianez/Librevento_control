<script lang="ts">
	import { user, fetchUser } from '../../stores/user';

	let name: string = '';
	let password: string = '';
	const login = async () => {
		try {
			const response = await fetch('http://localhost:8000/usuario/login', {
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

<div class="flex min-h-150 w-full items-center justify-center">
	<div
		class="items-between flex h-100 flex-col justify-center gap-10 rounded-2xl border-2 border-[#7A9660] p-15"
	>
		<h1 class="text-2xl font-bold">Inicio de Sesión</h1>
		<input
			type="text"
			name="username"
			placeholder="Usuario"
			class="text-center"
			bind:value={name}
			required
		/>
		<input
			type="password"
			name="password"
			placeholder="Contraseña"
			class="text-center"
			bind:value={password}
			required
		/>
		<button
			type="submit"
			class="cursor-pointer rounded-2xl bg-[#7A9660] p-2 text-white hover:bg-[#6b8755]"
			on:click|preventDefault={login}>Iniciar Sesión</button
		>
	</div>
</div>
