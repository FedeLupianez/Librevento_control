<script lang="ts">
	import { user } from '$lib/stores/user';
	import { fade } from 'svelte/transition';
	import Icon from '@iconify/svelte';
	import { API_ROUTES } from '$lib/routes';
	import { ROUTES } from '$lib/routes';
	import { goto } from '$app/navigation';
	import { theme } from '$lib/stores/theme';

	let email: string = '';
	let password: string = '';
	let show_error: boolean = false;
	let load: boolean = false;
	let view_password: boolean = false;

	const login = async () => {
		load = true;
		const response = await fetch(API_ROUTES.USER.LOGIN, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ user_email: btoa(email), password: btoa(password) }),
			credentials: 'include'
		});
		load = false;
		if (response.ok) {
			const data = await response.json();
			console.log('usuario logueado');
			user.set(data.user);
			show_error = false;
			goto(`${ROUTES.VOLTAGE}`); // Redireccionar automáticamente
		} else {
			console.log('Error al iniciar sesion');
			show_error = true;
			throw new Error('Login failed');
		}
	};
</script>

<svelte:head>
	<title>Iniciar Sesión</title>
	<meta name="description" content="Iniciar Sesión" />
</svelte:head>

<div class="relative flex min-h-screen flex-col items-center justify-center">
	<div class="z-10 flex h-full w-full flex-col items-center justify-start gap-5">
		<span class="text-5xl font-bold {$theme === 'dark' ? 'text-white' : 'text-black'}"
			>Inicia sesión</span
		>
		<input
			type="text"
			name="username"
			placeholder="Tu correo electrónico"
			class="
				w-full border-2
				{$theme == 'dark' ? 'border-white' : 'border-black'} px-4
				py-2 text-left text-[15px] {$theme == 'dark'
				? 'text-white'
				: 'text-black'} sm:w-1/2 lg:w-1/3 xl:w-1/4"
			bind:value={email}
			required
		/>
		<div class="relative w-full sm:w-1/2 lg:w-1/3 xl:w-1/4">
			<input
				type={view_password ? 'text' : 'password'}
				name="password"
				placeholder="Tu contraseña"
				class="
					w-full border-2
					{$theme == 'dark' ? 'border-white' : 'border-black'} px-4
					py-2 pr-12 text-left text-[15px] {$theme == 'dark' ? 'text-white' : 'text-black'}"
				bind:value={password}
				on:keypress={(e) => {
					if (e.key == 'Enter') login();
				}}
				required
			/>
			<button
				type="button"
				class="absolute top-1/2 right-3 h-5 w-5 -translate-y-1/2 text-gray-600 hover:text-gray-800"
				on:click={() => (view_password = !view_password)}
			>
				<Icon
					icon={view_password ? 'formkit:eye' : 'formkit:eyeclosed'}
					class={$theme === 'dark' ? 'text-white' : ''}
				/>
			</button>
		</div>
		<button
			in:fade={{ duration: 500 }}
			type="submit"
			class="w-full cursor-pointer bg-[#7A9660] p-2 text-white hover:bg-[#6b8755] sm:w-1/2 lg:w-1/3 xl:w-1/4"
			on:click|preventDefault={login}>Iniciar Sesión</button
		>
		<div class="flex flex-row items-center justify-center">
			{#if load}
				<Icon
					icon="eos-icons:loading"
					class="h-10 w-10 animate-spin {$theme === 'dark' ? 'text-white' : 'text-[#7A9660]'}"
				/>
			{/if}
			{#if show_error}
				<span in:fade={{ duration: 500 }} class="z-0 mr-2 bg-red-500 p-2 text-white"
					>Error al iniciar sesión</span
				>
			{/if}
		</div>
	</div>
	<img
		src="/images/plantita_decorativa_login_sin_fondo.svg"
		class="pointer-events-none absolute bottom-0 h-auto w-2xl opacity-70 select-none"
		alt="plantita decorativa"
	/>
</div>
