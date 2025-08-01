<script lang="ts">
	import { logoutUser, user } from '../stores/user';
	import Icon from '@iconify/svelte';

	let showProfile: boolean = false;
</script>

<div class={`group relative ${showProfile ? 'z-30' : ''}`}>
	<button class="relative z-20 cursor-pointer" on:click={() => (showProfile = !showProfile)}>
		{#if $user}
			<img
				src={$user.foto_perfil}
				alt="Foto de perfil"
				class="h-15 min-h-15 w-15 min-w-15 rounded-full"
			/>
		{:else}
			<Icon icon="bx:user" class="h-15 w-15 cursor-pointer rounded-full" />
		{/if}
	</button>

	{#if showProfile}
		<div
			class="absolute -top-3.5 -right-3.5 z-10 mt-1 min-w-52 flex-col rounded-md bg-[#ddd5d5] p-4 shadow-md"
		>
			<div class="flex flex-row items-center justify-around gap-5 border-b-1 border-black">
				{#if $user}
					{console.log($user)}
					<div class="flex flex-col items-center justify-center gap-1">
						<span class="text-center text-[#2f3e2f]">{$user.nombre}</span>
						<span class="text[#2f3e2f] text-center text-[1rem]">{$user.email}</span>
					</div>
				{:else}
					<span class="p-5">Usuario</span>
				{/if}
				<div class="h-15 w-15"></div>
			</div>

			<div class="flex flex-col items-center justify-center">
				{#if $user}
					<button
						class="flex w-full items-center justify-center gap-5 rounded-2xl px-4 py-2 font-bold text-white hover:bg-[#b4b1b1]"
					>
						<Icon icon="pepicons-pencil:gear" class="h-5 w-5" />
						<span class="rounded-2xl text-center">Configuración</span>
					</button>

					<button
						class="flex w-full items-center justify-center gap-5 rounded-2xl px-4 py-2 font-bold text-white hover:bg-[#b4b1b1]"
						on:click={logoutUser}
					>
						<Icon icon="bx:log-out" class="h-5 w-5" />
						<span class="rounded-2xl text-center text-[#c85d4d]">Cerrar Sesión</span>
					</button>
				{:else}
					<a
						href="/signup"
						class="flex w-full items-center justify-center gap-5 rounded-2xl px-4 py-2 font-bold text-white hover:bg-[#b4b1b1]"
					>
						<span class="rounded-2xl text-center text-white">Crear Cuenta</span>
					</a>
					<a
						href="/login"
						class="flex w-full items-center justify-center gap-5 rounded-2xl px-4 py-2 font-bold text-white hover:bg-[#b4b1b1]"
					>
						<span class="rounded-2xl text-center text-white">Iniciar Sesión</span>
					</a>
				{/if}
			</div>
		</div>
	{/if}
</div>
