<script lang="ts">
	import '@fontsource/gruppo';
	import '@fontsource/hammersmith-one';
	import Icon from '@iconify/svelte';
	import { ROUTES } from '$lib/routes';
	import ConstructionItem from './components/construction_item.svelte';
	import TechIcon from './components/tech_icon.svelte';
	import { onMount } from 'svelte';

	const sections = ['Armado', 'Software', 'Centro de Control', 'Repositorios', '¿Quienes somos?'];
	let is_scrolled = false;
	onMount(() => {
		window.addEventListener('scroll', () => {
			is_scrolled = window.scrollY > 0;
		});
	});
</script>

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
	<img
		src="https://placehold.co/600x400"
		alt="imagen fondo"
		class="aspect-video w-screen object-cover object-center"
	/>
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

<main class="mt-96 flex min-h-screen flex-col items-center justify-center gap-9 p-8">
	<section class="flex flex-row gap-5">
		<div class="flex w-1/2 flex-col items-center justify-center gap-5">
			<span class="paragraph w-full">
				La necesidad de nuevas formas de generar energía que no contaminen nuestro planeta nos llevó
				a construir sistemas basados en recursos renovables, que no generen nada -o casi nada- de
				desechos.
			</span>
			<span class="paragraph w-full">
				Librevento es una forma facil y economica de implementar este estilo de vida, con un
				sencillo armado y control total de lo generado.
			</span>
		</div>

		<div class="flex w-1/2 flex-col items-end">
			<span class="title front-bold text-5xl text-black">Indice</span>
			<div class="flex w-full flex-col items-end gap-1">
				{#each sections as section, i}
					<div class="flex w-4/5 items-start justify-between">
						<span class="text-2xl font-bold">{i + 1}.</span>
						<a href={`#${section}`} class="title text-2xl hover:cursor-pointer hover:text-[#7A9660]"
							>{section}</a
						>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<section class="flex flex-col gap-5" id="Armado">
		<div class="flex w-full justify-start">
			<span class="title text-5xl font-bold">1. Armado</span>
		</div>
		<ConstructionItem
			image_url={'https://placehold.co/400x600'}
			title="Palas diseño savonius"
			text="Esta parte del proyecto fue hecha con una impresora 3D con PETG (material de impresión 3D), elegimos este diseño vertical ya que tiene una forma que consiguió resultados de eficiencia mejores a muchos otros diseños, como también porque su construcción es sencilla y de bajo costo"
		/>
		<ConstructionItem
			image_url={'https://placehold.co/400x600'}
			title="Motores de corriente continua 12v"
			text="A estos componentes los rescatamos de una impresora vieja la cual no servía. Estos son los que generan la energía al momento de que las palas sean empujadas por el viento."
		/>
		<ConstructionItem
			image_url={'https://placehold.co/400x600'}
			title="Engranajes"
			text="Estas piezas son clave ya que gracias a ellas el movimiento de las palas se transmite a los motores. Constan de 3 (tres) engranajes hermanados impresos en 3D con el mismo material que las palas, siendo uno más grande, el cual está unido a las palas y otros dos menores que van unidos a los ejes de los motores. "
		/>
		<ConstructionItem
			image_url={'https://placehold.co/400x600'}
			title="Base, Tornillos y eje"
			text="
            La base es usada para sostener la estructura, esta también fue impresa en 3D junto con las palas. 
            Tornillos para fijar partes móviles del dispositivo.
            Y un eje de acero modificado por nosotros mismos con un torno.
         "
		/>
		<ConstructionItem
			image_url={'https://placehold.co/400x600'}
			title="Rulemanes"
			text="Uno más grande (de 3.8mm) que va en la base de la impresión de las palas, y otro más pequeño que va en la parte superior. Estos rulemanes se asientan en el eje, y con ellos se mantienen las palas. Pero no están fijados a este, siendo fácil de desmontar, lo cual ayuda a una fácil reparación y reemplazo de piezas."
		/>
		<ConstructionItem
			image_url={'https://placehold.co/400x600'}
			title="Soporte"
			text="Para los motores hecho por nosotros con distintas partes metálicas."
		/>
		<span class="title text-3xl"> Placa de desarrollo ESP32 con módulo WiFi integrado.</span>
		<span class="title text-3xl"> Cables</span>
		<ConstructionItem
			image_url={null}
			title=" Sensor de corriente LNA219"
			text="Para monitorear tanto el voltaje generado por los motores como los wats."
		/>
		<ConstructionItem
			image_url={null}
			title="Módulo Step-up"
			text="Para elevar el voltaje de la energía generada por los motores a un nivel apto para el uso."
		/>
		<ConstructionItem
			image_url={null}
			title="Regulador de voltaje casero"
			text="
				Compuesto por distintas piezas electrónicas como: Potenciómetro para regular su actuación.
				Regulador de tensión lm317. Resistencias de 10k."
		/>
	</section>

	<section class="flex w-full flex-col items-start justify-start gap-5" id="Software">
		<div class="flex flex-row items-center justify-start gap-2">
			<Icon icon="ph:arrow-down-thin" class="h-11 w-11 -rotate-45 transform" />
			<span class="title title p-2 text-5xl text-black"> Software </span>
		</div>
		<p class="paragraph">
			Podemos dividir el software desarrollado en dos bloques. El primer bloque sería el software
			para controlar la anteriormente mencionada placa de desarrollo esp32, con el cual en los
			primeros minutos de que este se haya activado relacionamos directamente el dispositivo físico
			con la base de datos donde guardamos las mediciones de la energía generada. Esto lo logramos
			por medio de una API propia de la cual se profundizará más adelante en el documento. Siguiendo
			con la utilización de la placa, la programamos con el lenguaje C++, utilizando un entorno de
			trabajo de PlatformIO, el cual nos facilitó la integración de dependencias, compilación de
			código y pruebas de este. El segundo de estos bloques es el relacionado con la página web para
			ver los datos del generador. Empezando a plantear esta parte del proyecto por el diseño, al
			cual lo hicimos en Canva teniendo en cuenta el tener una buena navegación y una buena
			presentación del producto. A la vez, empezamos a diseñar la base de datos que íbamos a
			requerir para almacenar la información, y cómo íbamos a acceder a ella, pensando también en
			las conexiones. Este bloque a la vez está dividido en el “Frontend” y el “Backend”, siendo la
			primera la parte visual de la página, donde utilizamos principalmente la tecnología “Svelte”
			junto con “Sveltekit” para llevar a cabo su desarrollo. Optamos por este framework (entorno de
			trabajo) debido a que tiene una sintaxis simple y su funcionamiento es fácil de aprender,
			siendo muy utilizada en el mundo laboral actual para el desarrollo de páginas web. Utilizamos
			a su vez distintas librerías que nos facilitaron la implementación de componentes gráficos
			para la representación de los datos, o recursos decorativos. En tanto al Backend, empezando a
			hablar de la base de datos, esta está diseñada en Postgresql, un motor de base de datos
			relacionales muy utilizado en la actualidad, como también la adaptamos a Mariadb, debido a que
			este otro motor es el que utiliza el servidor de la institución. Y para relacionar la base de
			datos con el resto de software creamos una API propia con el lenguaje de programación Python,
			junto con librerías especializadas en la creación de estas APIs, conexión a bases de datos,
			además de algunas que nos ayudaron a mantener un grado de seguridad tanto a la hora de
			desarrollar la aplicación como también a la hora de guardar datos sensibles, como lo podría
			ser el guardar la contraseña de las cuentas personales de los usuarios. Cabe añadir que además
			de las tecnologías anteriormente mencionadas utilizadas íntegramente para la creación de
			código, también utilizamos otras que nos facilitaron tareas o que nos ayudaron a mantener un
			órden a la hora de programar. Tales como : Git, para llevar un versionado del proyecto de
			forma correcta y ordenada, Github para almacenar el código y poder modificarlo tanto en
			nuestras casas como en el aula sin perder ningún cambio, Vercel para hospedar la página web,
			Render para desplegar nuestra API python en la nube y Neon como host para almacenar nuestra
			base de datos y poder acceder a ella a través de la nube. Por último, este proyecto está
			enfocado en ser un prototipo de una fuente de energía limpia y accesible, pero por el momento
			este no genera la electricidad necesaria para alimentar todo un hogar o una habitación. El
			enfoque que se debería adoptar para proyecto en un futuro debería de centrarse en asegurar una
			capacidad de generación de energía más grande y eficiente a la hora de entregarla.
		</p>
	</section>

	<section class="mt-5 flex flex-col gap-2" id="Centro de Control">
		<div class="flex flex-row gap-2">
			<span class="title text-5xl font-bold text-black">2.</span>
			<a href="/">
				<span class="title text-5xl font-bold text-black">Centro de control</span>
			</a>
		</div>
		<p class="paragraph">
			Como parte de las nuevas tecnologías integradas en nuestro aerogenerador, incorporamos una
			interfaz que facilita la interacción con la energía generada. El Centro de Control de
			Librevento permite visualizar, a través de gráficos, toda la información relevante sobre la
			actividad del generador a lo largo del día.
		</p>
	</section>

	<section class="mt-5 flex flex-col">
		<div class="flex flex-row items-center justify-start gap-2">
			<Icon icon="ph:arrow-down-thin" class="h-11 w-11 -rotate-45 transform" />
			<span class="title title p-2 text-5xl text-black"> Tutorial </span>
		</div>

		<div class="mb-10 flex h-56 w-full bg-[#7A9660]"></div>
		<div class="flex flex-col gap-3">
			<p class="paragraph">
				1. Pestaña “principal”: hace referencia a la sección que se visualiza en la imagen. En esta
				página se puede encontrar: un gráfico con la información de los voltios generados en la
				semana, un panel donde se señala el día con mayor voltios registrado y un gráfico de lo
				consumido en el día de la energía generada.
			</p>

			<p class="paragraph">
				2. Pestaña “estadisticas”: en la siguiente sección, se puede elegir entre las siguientes
				opciones: Consumo por día Consumo por mes En estas dos opciones, el usuario puede elegir la
				fecha exacta de la que quiere consultar los datos y se le mostrará un gráfico de los
				movimientos estadìsticos guardados.
			</p>

			<p class="paragraph">
				3. Pestaña “editar”: aca se encuentra la opción para cambiar el aspecto de las paginas al
				“modo oscuro”. También, se puede dirigir al menú de configuración de WIFI.
			</p>

			<p class="paragraph">
				4. Foto de perfil: si selecciona esta opción, el usuario encontrará: Editar datos de
				usuario. Cerrar sesión
			</p>

			<p class="paragraph">
				5. “Más información”: esta opción lo va a re-dirigir hacia un pequeño panel donde se podrá
				ver que características atmosfericas presentó el día más eficiente.
			</p>
		</div>
	</section>

	<section class="flex w-full flex-col gap-4" id="Repositorios">
		<div class="flex flex-row items-center justify-start gap-2">
			<span class="title text-5xl font-bold text-black">3.</span>
			<span class="title text-5xl font-bold text-black">Repositorios</span>
			<Icon icon="akar-icons:github-fill" class="h-10 w-10" />
		</div>
		<div class="flex w-full flex-row gap-4">
			<div class="flex h-48 w-full flex-col gap-2 border border-black p-5">
				<a
					href="https://github.com/FedeLupianez/Librevento_control"
					class="flex h-full flex-col items-start justify-start"
				>
					<span class="title text-4xl font-bold text-black">Centro de </span>
					<span class="title text-4xl font-bold text-black">Control</span>
				</a>
				<div class="flex h-auto w-1/2 flex-row items-center justify-between">
					<TechIcon icon_name="devicon:svelte" />
					<TechIcon icon_name="logos:python" />
					<TechIcon icon_name="devicon:fastapi" />
					<TechIcon icon_name="logos:postgresql" />
					<TechIcon icon_name="material-icon-theme:git" />
				</div>
			</div>
			<div class="flex h-48 w-full flex-col gap-2 border border-black p-5">
				<a
					href="https://github.com/FedeLupianez/Librevento_robotica"
					class="flex h-full flex-col items-start justify-start"
				>
					<span class="title text-4xl font-bold text-black">Código en </span>
					<span class="title text-4xl font-bold text-black">Placa ESP-32 </span>
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
		<span class="title text-5xl font-bold text-black">¿Quienes somos?</span>
		<p class="paragraph">
			Como ciudadanos y futuros técnicos, buscamos formas de combatir el calentamiento global desde
			la posicion que tenemos, siendo alumnos del Instituto Manuel de Falla. Elegimos para nuestro
			proyecto de robotica algo que, pensamos, tendria utilidad más alla de lo educativo.
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
