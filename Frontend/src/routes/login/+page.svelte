<script lang="ts">
	import { user, fetchUser } from '../../stores/user';
	import { fade } from 'svelte/transition';
	let email: string = '';
	let password: string = '';
	let show_error: boolean = false;
	let show_success: boolean = false;
	const login = async () => {
		try {
			const response = await fetch('http://localhost:8000/usuario/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email_usuario: email, clave: password }),
				credentials: 'include'
			});

			if (response.ok) {
				const data = await response.json();
				user.set(data);
				await fetchUser();
				show_error = false;
				show_success = true;
				// Cambio al usuario a la pagina principal
				// window.location.href = '/';
			} else {
				throw new Error('Login failed');
			}
		} catch (e) {
			console.log(e);
			show_error = true;
			show_success = false;
		}
	};
</script>

<div class="relative flex min-h-screen flex-col items-center justify-center">
	<div class="z-10 flex h-full w-full flex-col items-center justify-start gap-5">
		<span class="text-5xl font-bold text-black">Inicia sesión</span>
		<input
			type="text"
			name="username"
			placeholder="Tu correo electrónico"
			class="
				w-full border-2
				border-black px-4
				py-2 text-left text-[15px] sm:w-1/2 lg:w-1/3 xl:w-1/4"
			bind:value={email}
			required
		/>
		<input
			type="password"
			name="password"
			placeholder="Tu contraseña"
			class="
				w-full border-2
				border-black px-4
				py-2 text-left text-[15px] sm:w-1/2 lg:w-1/3 xl:w-1/4"
			bind:value={password}
			required
		/>
		<button
			type="submit"
			class="w-full cursor-pointer bg-[#7A9660] p-2 text-white hover:bg-[#6b8755] sm:w-1/2 lg:w-1/3 xl:w-1/4"
			on:click|preventDefault={login}>Listo</button
		>
		<div class="flex flex-row items-center justify-center">
			{#if show_error}
				<span in:fade={{ duration: 500 }} class="z-0 mr-2 bg-red-500 text-white"
					>Error al iniciar sesión</span
				>
			{/if}
			{#if show_success}
				<button
					in:fade={{ duration: 500 }}
					class="z-0 mr-2 cursor-pointer bg-[#7A9660] text-white"
					on:click={() => (window.location.href = '/')}
				>
					Ir a la página principal
				</button>
			{/if}
		</div>
	</div>
	<img
		src="/public/images/plantita_decorativa_login_sin_fondo.svg"
		class="pointer-events-none absolute bottom-0 h-auto w-2xl opacity-70 select-none"
		alt="plantita decorativa"
	/>
</div>
