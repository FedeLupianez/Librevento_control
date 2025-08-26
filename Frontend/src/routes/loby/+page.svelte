<script lang="ts">
	import '@fontsource/gruppo';
	import '@fontsource/hammersmith-one';
	import Icon from '@iconify/svelte';
</script>

<section class="absolute top-0 left-0 mb-5 flex h-96 w-screen items-center overflow-hidden">
	<img
		src="https://media.canva.com/v2/image-resize/format:JPG/height:480/quality:92/uri:ifs%3A%2F%2FM%2Fcfe95081-9dc4-424e-b0dc-a6b038033213/watermark:F/width:640?csig=AAAAAAAAAAAAAAAAAAAAAMN6INdxeZz035d5Qj4f52ho39BnXegbEDBJRQy21UUh&exp=1756231169&osig=AAAAAAAAAAAAAAAAAAAAAPzecGw1T4gk69FA7RKwsd-pQqU0Psq41h3YG2RD3rkP&signer=media-rpc&x-canva-quality=screen"
		alt="imagen fondo"
		class="aspect-video w-screen object-cover object-center"
	/>
	<div class="absolute right-15 bottom-5 flex flex-col">
		<span class="text-3xl">Librevento</span>
		<div class="flex flex-row items-center justify-center gap-5">
			<button>Crear Cuenta</button>
			<button>Iniciar sesion</button>
		</div>
	</div>
</section>

<main class="mt-96 flex min-h-screen flex-col items-center justify-center gap-4 p-8">
	<section class="flex flex-col gap-2">
		<div class="flex flex-row gap-2">
			<span class="title text-5xl text-black">2.</span>
			<span class="title text-5xl text-black">Centro de control</span>
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

	<section class="flex w-full flex-col gap-4">
		<div class="flex flex-row gap-2">
			<span class="title title text-5xl text-black">3.</span>
			<span class="title title text-5xl text-black">Repositorios</span>
		</div>
		<div class="flex w-full flex-row gap-4">
			<div class="flex h-48 w-full flex-col gap-2 border border-black p-5">
				<a
					href="https://github.com/FedeLupianez/Librevento-control"
					class="flex h-full flex-col items-start justify-start"
				>
					<span class="title title text-4xl font-bold text-black">Centro de </span>
					<span class="title title text-4xl font-bold text-black">Control</span>
				</a>
			</div>
			<div class="flex h-48 w-full flex-col gap-2 border border-black p-5">
				<a
					href="https://github.com/FedeLupianez/Librevento-robotica"
					class="flex h-full flex-col items-start justify-start"
				>
					<span class="title title text-4xl font-bold text-black">Código en </span>
					<span class="title title text-4xl font-bold text-black">Placa ESP-32 </span>
				</a>
			</div>
		</div>
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
