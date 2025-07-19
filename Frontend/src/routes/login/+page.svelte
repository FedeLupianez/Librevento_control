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

<div class="relative min-h-screen items-center justify-center">
	<img
		src="/public/plantita_decorativa_login.png"
		class="pointer-events-none absolute bottom-0 left-0 h-auto w-full opacity-70 select-none"
		alt="plantita decorativa"
	/>

	<div class="flex flex-col justify-center gap-5">
		<h1 class="text-4x1 font-bold">Inicia sesión</h1>
		<input
			type="text"
			name="username"
			placeholder="Tu nombre de usuario"
			class="
				w-[375px]
				border border-gray-800
				px-4 py-2
				text-left text-[15px]"
			bind:value={name}
			required
		/>
		<input
			type="password"
			name="password"
			placeholder="Tu contraseña"
			class="
				w-[375px]
				border border-gray-800
				px-4 py-2
				text-left text-[15px]"
			bind:value={password}
			required
		/>
		<button
			type="submit"
			class="cursor-pointer bg-[#7A9660] p-2 text-white hover:bg-[#6b8755]"
			on:click|preventDefault={login}>Listo</button
		>
	</div>
</div>
