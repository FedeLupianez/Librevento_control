<script lang="ts">
	import { logoutUser, user } from '../stores/user';
	import Icon from '@iconify/svelte';

	let showProfile: boolean = false;
</script>

<div class="group relative">
	<button class="cursor-pointer" on:click={() => (showProfile = !showProfile)}>
		{#if $user}
			{console.log(`Url de la foto de perfil : ${$user.foto_perfil}`)}
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
			class="absolute -top-4.5 -right-4.5 mt-1 min-w-52 flex-col rounded-md bg-[#b9c3c8] p-0.5 shadow-md"
		>
			<div class="flex flex-row items-center justify-around">
				{#if $user}
					<span class="p-5">{$user.nombre}</span>
				{:else}
					<span class="p-5">Usuario</span>
				{/if}
				<button class="flex cursor-pointer flex-row" on:click={() => (showProfile = !showProfile)}>
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
			</div>

			<div class="flex flex-col items-center justify-center">
				{#if $user}
					<button
						class="flex w-full items-center justify-center rounded-2xl px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
						on:click={logoutUser}
					>
						<Icon icon="bx:log-out" class="h-5 w-5" />
						<span class="rounded-2xl text-center text-red-500">Cerrar Sesión</span>
					</button>
				{:else}
					<a
						href="/login"
						class="flex w-full items-center justify-center rounded-2xl px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
					>
						<span class="rounded-2xl text-center text-white">Iniciar Sesión</span>
					</a>
				{/if}
			</div>
		</div>
	{/if}
</div>
