<script lang="ts">
	import '@fontsource/gruppo';
	import '@fontsource/hammersmith-one';
	import Icon from '@iconify/svelte';
	import { ROUTES } from '$lib/routes';
	import TechIcon from './components/tech_icon.svelte';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';

	$: text_color = $theme === 'dark' ? 'text-white' : 'text-black';

	const sections = ['Armado', 'Software', 'Centro de Control', 'Repositorios', '¿Quienes somos?'];
	let is_scrolled = false;
	onMount(() => {
		window.addEventListener('scroll', () => {
			is_scrolled = window.scrollY > 0;
		});
	});
</script>

<svelte:head>
	<title>Librevento</title>
	<meta name="description" content="Nuestro proyecto" />
</svelte:head>

{#if is_scrolled}
	<a href="#top" class="position fixed top-5 right-5">
		<button class="rounded-full border-2 border-[#7A9660] hover:cursor-pointer hover:bg-[#7A9660]">
			<Icon
				icon="material-symbols:arrow-upward-rounded"
				class="h-10 w-10 text-[#7A9660] hover:text-white"
			/>
		</button>
	</a>
{/if}
<section class="absolute top-0 left-0 mb-5 flex h-96 w-screen items-center overflow-hidden">
	<img src="/images/Fondo_loby.png" alt="imagen fondo" class="aspect-video w-screen" />
	<div class="absolute right-15 bottom-5 flex flex-col">
		<span class="title text-9xl text-white">Librevento</span>
		<div class="flex flex-row items-center justify-end gap-5 px-3">
			<button
				class=" rounded-none border-2 border-white px-4 py-2 text-white hover:cursor-pointer hover:bg-white hover:text-black"
				on:click={() => {
					window.location.href = ROUTES.USER.SIGN_UP;
				}}>Crear Cuenta</button
			>
			<button
				class="rounded-none border-2 border-white px-4 py-2 text-white hover:cursor-pointer hover:bg-white hover:text-black"
				on:click={() => {
					window.location.href = ROUTES.USER.LOGIN;
				}}
			>
				Iniciar sesion
			</button>
		</div>
	</div>
</section>

<main class="mt-96 flex min-h-screen flex-col items-center justify-center gap-9 p-20">
	<section class="flex flex-row gap-5">
		<div class="flex w-1/2 flex-col items-center justify-center gap-5">
			<span class="paragraph w-full {text_color}">
				La necesidad de nuevas formas de generar energía que no contaminen nuestro planeta nos llevó
				a construir sistemas basados en recursos renovables, que no generen nada -o casi nada- de
				desechos.
			</span>
			<span class="paragraph w-full {text_color}">
				Librevento es una forma facil y economica de implementar este estilo de vida, con un
				sencillo armado y control total de lo generado.
			</span>
		</div>

		<div class="flex w-1/2 flex-col items-end">
			<span class="title front-bold text-5xl text-black {text_color}">Indice</span>
			<div class="flex w-full flex-col items-end gap-1">
				{#each sections as section, i}
					<div class="flex w-4/5 items-start justify-between">
						<span class="text-2xl font-bold {text_color}">{i + 1}.</span>
						<a
							href={`#${section}`}
							class="title text-2xl hover:cursor-pointer hover:text-[#7A9660] {text_color}"
							>{section}</a
						>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<section class="flex w-full flex-col items-center justify-center gap-5" id="Armado">
		<div class="flex w-full flex-col justify-start">
			<span class="title text-5xl font-bold {text_color}">1. Armado y Software</span>
			<p class="paragraph w-full {text_color}">
				Accede al siguiente PDF para apreciar con exactitud qué materiales usamos y qué tecnologías
				implementamos:
			</p>
		</div>

		<a href="/armado_software.pdf">
			<div
				class="flex h-full w-full flex-row items-center justify-start gap-6 border-1 {$theme ==
				'dark'
					? 'border-white'
					: 'border-black'} p-10"
			>
				<Icon icon="uiw:file-pdf" class="h-auto w-1/3 {text_color}" />
				<span class="title text-5xl font-bold {text_color}">Haga click para descargar</span>
			</div>
		</a>
	</section>

	<section class="mt-5 flex flex-col gap-2" id="Centro de Control">
		<div class="flex flex-row gap-2">
			<span class="title text-5xl font-bold {text_color} ">2.</span>
			<a href="/meditions/voltage">
				<span class="title text-5xl font-bold {text_color}">Centro de control</span>
			</a>
		</div>
		<p class="paragraph {text_color}">
			Como parte de las nuevas tecnologías integradas en nuestro aerogenerador, incorporamos una
			interfaz que facilita la interacción con la energía generada. El Centro de Control de
			Librevento permite visualizar, a través de gráficos, toda la información relevante sobre la
			actividad del generador a lo largo del día.
		</p>
	</section>

	<section class="mt-5 flex flex-col gap-5">
		<div class="flex flex-row items-center justify-start gap-2">
			<Icon icon="ph:arrow-down-thin" class="h-11 w-11 -rotate-45 transform {text_color}" />
			<span class="title title p-2 text-5xl {text_color}"> Tutorial </span>
		</div>

		<img src="/images/Tutorial.png" alt="Screenshot" class="h-auto w-full" />

		<div class="flex flex-col gap-3">
			<p class="paragraph {text_color}">
				1. Pestaña “principal”: hace referencia a la sección que se visualiza en la imagen. En esta
				página se puede encontrar: un gráfico con la información de los voltios generados en la
				semana, un panel donde se señala el día con mayor voltios registrado y un gráfico de lo
				consumido en el día de la energía generada.
			</p>

			<p class="paragraph {text_color}">
				2. Pestaña “estadisticas”: en la siguiente sección, se puede elegir entre las siguientes
				opciones: Consumo por día Consumo por mes En estas dos opciones, el usuario puede elegir la
				fecha exacta de la que quiere consultar los datos y se le mostrará un gráfico de los
				movimientos estadìsticos guardados.
			</p>

			<p class="paragraph {text_color}">
				3. Pestaña “editar”: aca se encuentra la opción para cambiar el aspecto de las paginas al
				“modo oscuro”. También, se puede dirigir al menú de configuración de WIFI.
			</p>

			<p class="paragraph {text_color}">
				4. Foto de perfil: si selecciona esta opción, el usuario encontrará: Editar datos de
				usuario. Cerrar sesión
			</p>

			<p class="paragraph {text_color}">
				5. “Más información”: esta opción lo va a re-dirigir hacia un pequeño panel donde se podrá
				ver que características atmosfericas presentó el día más eficiente.
			</p>
		</div>
	</section>

	<section class="flex w-full flex-col gap-4" id="Repositorios">
		<div class="flex flex-row items-center justify-start gap-2">
			<span class="title text-5xl font-bold {text_color}">3.</span>
			<span class="title text-5xl font-bold {text_color}">Repositorios</span>
			<Icon icon="akar-icons:github-fill" class="h-10 w-10 {text_color}" />
		</div>
		<div class="flex w-full flex-row gap-4">
			<div
				class="flex h-48 w-full flex-col gap-2 border {$theme === 'dark'
					? 'border-white'
					: 'border-black'} p-5"
			>
				<a
					href="https://github.com/FedeLupianez/Librevento_control"
					class="flex h-full flex-col items-start justify-start"
				>
					<span class="title text-4xl font-bold {text_color}">Centro de </span>
					<span class="title text-4xl font-bold {text_color}">Control</span>
				</a>
				<div class="flex h-auto w-1/2 flex-row items-center justify-between">
					<TechIcon icon_name="devicon:svelte" />
					<TechIcon icon_name="logos:python" />
					<TechIcon icon_name="devicon:fastapi" />
					<TechIcon icon_name="logos:postgresql" />
					<TechIcon icon_name="material-icon-theme:git" />
				</div>
			</div>
			<div
				class="flex h-48 w-full flex-col gap-2 border {$theme === 'dark'
					? 'border-white'
					: 'border-black'} p-5"
			>
				<a
					href="https://github.com/FedeLupianez/Librevento_robotica"
					class="flex h-full flex-col items-start justify-start"
				>
					<span class="title text-4xl font-bold text-black {text_color}">Código en </span>
					<span class="title text-4xl font-bold text-black {text_color}">Placa ESP-32 </span>
				</a>
				<div class="flex h-auto w-1/2 flex-row items-center justify-between">
					<TechIcon icon_name="vscode-icons:file-type-cpp2" />
					<TechIcon icon_name="vscode-icons:file-type-platformio" />
					<TechIcon icon_name="skill-icons:arduino" />
					<TechIcon icon_name="material-icon-theme:git" />
				</div>
			</div>
		</div>
	</section>
	<section id="¿Quienes somos?" class="flex flex-col">
		<span class="title text-5xl font-bold text-black {text_color}">¿Quienes somos?</span>
		<p class="paragraph {text_color}">
			Como ciudadanos y futuros técnicos, buscamos formas de combatir el calentamiento global desde
			la posición que tenemos, siendo alumnos del Instituto Manuel de Falla. Elegimos para nuestro
			proyecto de robótica algo que, pensamos, tendría utilidad más allá de lo educativo.
		</p>
	</section>
</main>

<style>
	.title {
		font-family: 'Gruppo';
	}
	.paragraph {
		font-family: 'Hammersmith One';
	}
</style>
