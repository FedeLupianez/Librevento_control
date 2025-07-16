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

<div class="flex w-full min-h-150 justify-center items-center">
	<div class="flex flex-col justify-center gap-5">
		<h1 class="text-4x1 font-bold">Inicia sesión</h1>
		<input 
			type="text" 
			name="username" 
			placeholder="Tu nombre de usuario" 
			class="
				text-left 
				border border-gray-800
				px-4 py-2 
				text-[15px] w-[375px]" 
			bind:value={name} required 
			/>
		<input 
			type="password" 
			name="password" 
			placeholder="Tu contraseña" 
			class="
				text-left 
				border border-gray-800
				px-4 py-2 
				text-[15px] w-[375px]" 
			bind:value={password} required />
		<button type="submit" class="bg-[#7A9660] text-white  p-2 cursor-pointer hover:bg-[#6b8755]" on:click|preventDefault={login}>Listo</button>
	</div>
</div>
