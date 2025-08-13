<script lang="ts">
	import Icon from '@iconify/svelte';
	import { onDestroy, onMount } from 'svelte';
	import { user, fetchUser, logoutUser } from '../stores/user';
	import UserProfileButton from './UserProfileButton.svelte';
	import DropDownButton from './DropDownButton.svelte';
	import { ROUTES } from '$lib/routes';

	let showMobile = false;
	let unsubscribe: () => void;

	function updateShow() {
		showMobile = window.innerWidth < 900;
	}

	let title: string = 'Bienvenido';
	function setTitle() {
		if (!$user) return;
		let sex: Record<string, string> = {
			male: 'Bienvenido',
			female: 'Bienvenida',
			unknown: 'Hola'
		};
		return sex[$user.sexo];
	}

	onMount(() => {
		unsubscribe = user.subscribe(async ($user) => {
			if (!$user) fetchUser();
			updateShow();
			setTitle();
			window.addEventListener('resize', updateShow);

			return () => {
				window.removeEventListener('resize', updateShow);
			};
		});
	});

	onDestroy(() => {
		if (unsubscribe) unsubscribe();
	});
</script>

{#if !showMobile}
	<div class="flex flex-row items-center justify-between border-b-0 border-b-[#2f3e2f] px-15 py-5">
		<h1 class="mr-15 items-center text-center">
			{#if !$user}
				<span class="text-[#2f3e2f]">{title}</span>
			{:else}
				<span class="text-[#2f3e2f]">
					{title}
				</span>
				<span class="text-[#c2b280]">{$user.nombre}</span>
			{/if}
		</h1>

		<div class="flex flex-row items-center gap-x-20 text-lg">
			<button class="flex cursor-pointer flex-row items-center justify-center gap-1.5 font-bold">
				principal
				<Icon icon="bx:leaf" class="h-5 w-5" />
			</button>

			<DropDownButton text="estadísticas" mode="hover">
				<slot slot="menu">
					<div class="mt-1 flex w-full min-w-52 flex-col rounded-md bg-[#7A9660] shadow-md">
						<a
							href={`${ROUTES.VOLTAGE}`}
							class="rounded-t-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
						>
							<span class="text-white">Voltaje Generado</span>
						</a>

						<a
							href={`${ROUTES.CONSUMPTION}`}
							class="rounded-t-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
						>
							<span class="text-white">Consumo por día</span>
						</a>

						<a
							href={`${ROUTES.CONSUMPTION}`}
							class="px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
						>
							<span class="text-white">Consumo por mes</span>
						</a>

						<a
							href={`${ROUTES.ALERTS}`}
							class="rounded-b-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
						>
							<span class="text-white">Alertas de consumo</span>
						</a>
					</div>
				</slot>
			</DropDownButton>

			<DropDownButton text="editar" mode="hover">
				<slot slot="menu">
					<div class="mt-1 flex w-full min-w-52 flex-col rounded-md bg-[#7A9660] shadow-md">
						<a
							href={`${ROUTES.USER.LOGIN}`}
							class="rounded-t-md px-4 py-2 font-bold hover:bg-[#6b8755]"
						>
							<span class="text-white">Iniciar Sesión</span>
						</a>
						<a
							href={`${ROUTES.USER.SIGN_UP}`}
							class="rounded-b-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
						>
							<span class="text-white">Crear Cuenta</span>
						</a>
					</div>
				</slot>
			</DropDownButton>
			<UserProfileButton />
		</div>
	</div>
	<div class="h-0.5 w-228 bg-gray-500"></div>
{:else}
	<div
		class="mt-4 flex flex-row items-center justify-around rounded-md bg-[#f5f5f5] p-4 font-bold text-[#2f3e2f] shadow"
	>
		<div class="flex flex-col items-center justify-center">
			<h1 class="items-center text-center">
				{#if !$user}
					<span class="text-[#2f3e2f]">{title}</span>
				{:else}
					<span class="text-[#2f3e2f]">
						{title}
					</span>
					<span class="text-[#c2b280]">{$user.nombre}</span>
				{/if}
			</h1>
			<div class="flex flex-row items-center justify-around gap-4">
				<button class="flex cursor-pointer flex-row items-center justify-center gap-1.5 font-bold">
					principal
					<Icon icon="bx:leaf" class="h-5 w-5" />
				</button>
				<DropDownButton text="estadísticas" mode="button">
					<slot slot="menu">
						<div class="mt-1 flex w-full min-w-52 flex-col rounded-md bg-[#7A9660] shadow-md">
							<a
								href={`${ROUTES.VOLTAGE}`}
								class="rounded-t-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
							>
								<span class="text-white">Voltaje Generado</span>
							</a>

							<a
								href={`${ROUTES.CONSUMPTION}`}
								class="rounded-t-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
							>
								<span class="text-white">Consumo por día</span>
							</a>

							<a
								href={`${ROUTES.CONSUMPTION}`}
								class="px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
							>
								<span class="text-white">Consumo por mes</span>
							</a>

							<a
								href={`${ROUTES.ALERTS}`}
								class="rounded-b-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
							>
								<span class="text-white">Alertas de consumo</span>
							</a>
						</div>
					</slot>
				</DropDownButton>

				<DropDownButton text="editar" mode="button">
					<slot slot="menu">
						<div class="mt-1 flex w-full min-w-52 flex-col rounded-md bg-[#7A9660] shadow-md">
							<a
								href={`${ROUTES.USER.LOGIN}`}
								class="rounded-t-md px-4 py-2 font-bold hover:bg-[#6b8755]"
							>
								<span class="text-white">Iniciar Sesión</span>
							</a>
							<a
								href={`${ROUTES.USER.SIGN_UP}`}
								class="rounded-b-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
							>
								<span class="text-white">Crear Cuenta</span>
							</a>
							<button
								class="rounded-b-md px-4 py-2 font-bold text-white hover:bg-[#6b8755]"
								on:click={logoutUser}>Cerrar Sesión</button
							>
						</div>
					</slot>
				</DropDownButton>
			</div>
		</div>
		<UserProfileButton />
	</div>
	<div class="h-0.5 bg-gray-500"></div>
{/if}
