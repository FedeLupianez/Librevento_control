<script lang="ts">
	import type { User } from '../types/user';
	import Icon from '@iconify/svelte';
	import flechita from '/public/flechita.svg';

	export let user: User | null;
</script>

<div
	class="container flex flex-row items-center justify-between border-b-0 border-b-[#2f3e2f] px-15 py-5"
>
	<h1 class="mr-15 items-center text-center">
		{#if !user}
			<span class="text-[#2f3e2f]">Bienvenido</span>
		{:else}
			<span class="text-[#2f3e2f]">
				{#if user.sex == 'hombre'}
					Bienvenido,
				{:else}
					Bienvenida,
				{/if}
			</span>
			<span class="text-[#c2b280]">{user.name}</span>
		{/if}
	</h1>

	<div class="flex gap-x-20 text-lg">
		<button class="flex cursor-pointer flex-row items-center justify-center gap-1.5 font-bold">
			principal
			<Icon icon="bx:leaf" class="h-5 w-5" />
		</button>
		<div class="group relative">
			<!-- se hace una familia uwu de los div adentro -->
			<button class="flex cursor-pointer items-center gap-1 font-bold text-[#2f3e2f]">
				estadísticas
				<img src={flechita} alt="flechita" class="-top-0.4 relative h-3.5 w-3.5" />
			</button>

			<!-- botón gris -->
			<div
				class="absolute -top-1 left-0 z-10 hidden rounded-md bg-[#b9c3c8] px-3 py-1 group-hover:block"
			>
				<span class="font-bold text-[#2f3e2f]">estadísticas</span>
			</div>

			<!-- Menú desplegable -->
			<div
				class="absolute left-0 z-20 mt-1 hidden w-52 flex-col rounded-md bg-[#7A9660] shadow-md group-hover:flex"
			>
				<a
					href="/consumo-dia"
					class="rounded-t-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]">Consumo por día</a
				>
				<a href="/consumo-mes" class="px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
					>Consumo por mes</a
				>
				<a href="/alertas" class="rounded-b-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
					>Alertas de consumo</a
				>
			</div>
		</div>
		<button class="flex cursor-pointer flex-row items-center justify-center gap-1 font-bold">
			editar
			<img src={flechita} alt="flechita" class="-top-0.4 relative h-3.5 w-3.5" />
		</button>
	</div>

	<button class="cursor-pointer">
		{#if user}
			<img src={user.imageUrl} alt="Foto de perfil" class="h-10 w-10 rounded-full" />
		{:else}
			<Icon icon="bx:user" class="h-10 w-10 cursor-pointer rounded-full" />
		{/if}
	</button>
</div>

<div class="h-0.5 w-228 bg-gray-500"></div>
