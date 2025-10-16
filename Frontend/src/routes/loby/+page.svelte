<script lang="ts">
	import '@fontsource/gruppo';
	import '@fontsource/hammersmith-one';
	import Icon from '@iconify/svelte';
	import { ROUTES } from '$lib/routes';
	import TechIcon from './components/tech_icon.svelte';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';

	$: text_color = $theme === 'dark' ? 'text-white' : 'text-black';

	const sections = ['Armado y Software', 'Centro de Control', 'Repositorios', '¿Quienes somos?'];
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
		<button class="rounded-full border-0 hover:cursor-pointer hover:bg-[#7A9660]">
			<Icon
				icon="material-symbols:arrow-upward-rounded"
				class="h-10 w-10 text-[#7A9660] hover:text-white"
			/>
		</button>
	</a>
{/if}
<section class="absolute top-0 left-0 flex h-auto max-h-96 w-screen items-center overflow-hidden">
	<img src="/images/Fondo_loby.png" alt="imagen fondo" class="h-auto w-full object-cover" />
	<div class="absolute right-5 bottom-5 flex flex-col items-end text-right">
		<span class="title text-6xl text-white sm:text-8xl md:text-9xl">Librevento</span>
		<div class="mt-2 flex flex-row flex-wrap justify-end gap-3 text-white">
			<button
				class="rounded-none border-2 border-white px-4 py-2 hover:cursor-pointer hover:bg-white hover:text-black"
				on:click={() => (window.location.href = ROUTES.USER.SIGN_UP)}
			>
				Crear Cuenta
			</button>
			<button
				class="rounded-none border-2 border-white px-4 py-2 hover:cursor-pointer hover:bg-white hover:text-black"
				on:click={() => (window.location.href = ROUTES.USER.LOGIN)}
			>
				Iniciar sesión
			</button>
			<button
				class="rounded-none border-2 border-white px-4 py-2 hover:cursor-pointer hover:bg-white hover:text-black"
				on:click={() => (window.location.href = ROUTES.VOLTAGE)}
			>
				Centro
			</button>
		</div>
	</div>
</section>

<main
	class="mt-96 flex min-h-screen flex-col items-center justify-center gap-24 overflow-y-auto scroll-smooth p-10 md:p-20"
>
	<section class="flex flex-row gap-5">
		<div class="paragraph flex w-1/2 flex-col items-center justify-center gap-5 {text_color}">
			<p class="w-full">
				La necesidad de nuevas formas de generar energía que no contaminen nuestro planeta nos llevó
				a construir sistemas basados en recursos renovables, que no generen nada -o casi nada- de
				desechos.
			</p>
			<p class="w-full">
				Librevento es una forma fácil y económica de implementar este estilo de vida, con un
				sencillo armado y control total de lo generado.
			</p>
		</div>

		<div class="flex w-1/2 flex-col items-end {text_color}">
			<span class="title front-bold text-5xl">Indice</span>
			<div class="flex w-full flex-col items-end gap-1">
				{#each sections as section, i}
					<div class="flex w-4/5 items-start justify-between text-2xl">
						<span class="font-bold">{i + 1}.</span>
						<a href={`#${section}`} class="title hover:cursor-pointer hover:text-[#7A9660]"
							>{section}</a
						>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<section class="flex w-full flex-col items-center justify-center gap-5" id="Armado y Software">
		<div class="flex w-full flex-col justify-start {text_color}">
			<span class="title text-5xl font-bold">1. Armado y Software</span>
			<p class="paragraph w-full">
				Accede al siguiente PDF para apreciar con exactitud qué materiales usamos y qué tecnologías
				implementamos:
			</p>
		</div>

		<a href="/armado_software.pdf" target="_blank">
			<div
				class="flex h-full w-full flex-row items-center justify-start gap-6 border-1 {$theme ==
				'dark'
					? 'border-white'
					: 'border-black'} p-10 {text_color}"
			>
				<Icon icon="teenyicons:pdf-outline" class="h-auto w-1/5" />
				<span class="title text-5xl font-bold">Haga click para descargar</span>
			</div>
		</a>
	</section>

	<section class="mt-5 flex flex-col gap-2" id="Centro de Control">
		<div class="flex flex-row gap-2 {text_color}">
			<span class="title text-5xl font-bold">2.</span>
			<a href="/meditions/voltage">
				<span class="title text-5xl font-bold">Centro de control</span>
			</a>
		</div>
		<p class="paragraph">
			Como parte de las nuevas tecnologías integradas en nuestro aerogenerador, incorporamos una
			interfaz que facilita la interacción con la energía generada. El Centro de Control de
			Librevento permite visualizar, a través de gráficos, toda la información relevante sobre la
			actividad del generador a lo largo del día.
		</p>
	</section>

	<section class="mt-5 flex flex-col gap-5">
		<div class="flex flex-row items-center justify-start gap-2 {text_color}">
			<Icon icon="ph:arrow-down-thin" class="h-11 w-11 -rotate-45 transform" />
			<span class="title title p-2 text-5xl"> Tutorial </span>
		</div>

		<img
			src="/images/Tutorial.png"
			alt="Screenshot"
			class="h-auto w-full border-1 border-[#7A9660]"
		/>

		<div class="flex flex-col gap-3 {text_color} paragraph">
			<p>
				1. Pestaña “principal”: hace referencia a la sección que se visualiza en la imagen. En esta
				página se puede encontrar: un gráfico con la información de los voltios generados en la
				semana, un panel donde se señala el día con mayor voltios registrado y un gráfico de lo
				consumido en el día de la energía generada.
			</p>

			<p>
				2. Pestaña “estadísticas”: en la siguiente sección, se puede elegir entre las siguientes
				opciones: Consumo por día Consumo por mes En estas dos opciones, el usuario puede elegir la
				fecha exacta de la que quiere consultar los datos y se le mostrará un gráfico de los
				movimientos estadísticos guardados.
			</p>

			<p>
				3. Pestaña “editar”: acá se encuentra la opción para cambiar el aspecto de las paginas al
				“modo oscuro”. También, se puede dirigir al menú de configuración de WIFI.
			</p>

			<p>
				4. Foto de perfil: si selecciona esta opción, el usuario encontrará: Editar datos de
				usuario. Cerrar sesión
			</p>

			<p>
				5. “Más información”: esta opción lo va a re-dirigir hacia un pequeño panel donde se podrá
				ver que características atmosféricas presentó el día más eficiente.
			</p>
		</div>
	</section>

	<section class="flex w-full flex-col gap-4" id="Repositorios">
		<div class="flex flex-row items-center justify-start gap-2 {text_color}">
			<span class="title text-5xl font-bold {text_color}">3.</span>
			<span class="title text-5xl font-bold {text_color}">Repositorios</span>
			<Icon icon="akar-icons:github-fill" class="h-10 w-10 {text_color}" />
		</div>
		<div class="flex w-full flex-col gap-4 md:flex-row">
			<div
				class="flex h-48 w-full flex-col gap-2 border {$theme === 'dark'
					? 'border-white'
					: 'border-black'} relative p-5 {text_color}"
			>
				<a
					href="https://github.com/FedeLupianez/Librevento_control"
					class="flex h-full flex-col items-start justify-start"
				>
					<span class="title text-4xl font-bold">Centro de </span>
					<span class="title text-4xl font-bold">Control</span>
				</a>
				<Icon
					icon="stash:leaf-light"
					class="absolute right-2 bottom-3 h-auto w-1/4 -rotate-45 md:top-3"
				/>
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
					: 'border-black'} p-5 {text_color} relative"
			>
				<a
					href="https://github.com/FedeLupianez/Librevento_robotica"
					class="title flex h-full flex-col items-start justify-start text-4xl font-bold"
				>
					<span class="title">Código en </span>
					<span class="title">Placa ESP-32 </span>
				</a>
				<Icon
					icon="stash:leaf-light"
					class="absolute right-2 bottom-3 h-auto w-1/4 -rotate-45 md:top-3"
				/>
				<div class="flex h-auto w-1/2 flex-row items-center justify-between">
					<TechIcon icon_name="vscode-icons:file-type-cpp2" />
					<TechIcon icon_name="vscode-icons:file-type-platformio" />
					<TechIcon icon_name="skill-icons:arduino" />
					<TechIcon icon_name="material-icon-theme:git" />
				</div>
			</div>
		</div>
	</section>
	<section id="¿Quienes somos?" class="flex flex-col {text_color}">
		<span class="title text-5xl font-bold">¿Quienes somos?</span>
		<p>
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

	p {
		font-family: 'Hammersmith One';
	}
</style>
