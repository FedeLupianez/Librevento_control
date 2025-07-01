<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart } from 'chart.js/auto';

	let canvas: HTMLCanvasElement;
	let chart: Chart | null = null;

	// Datos y configuración del gráfico
	const data = {
		labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
		datasets: [
			{
				label: 'Ventas',
				data: [10, 20, 30, 25, 40],
				borderColor: 'blue',
				backgroundColor: 'lightblue',
				fill: false,
				tension: 0.1
			}
		]
	};

	const options = {
		responsive: true,
		maintainAspectRatio: false
	};

	onMount(() => {
		chart = new Chart(canvas, {
			type: 'line',
			data: data,
			options
		});
		console.log(chart);

		return () => {
			chart?.destroy(); // Limpia el gráfico al desmontar el componente
		};
	});
</script>

<div class="chart-container">
	<canvas bind:this={canvas}></canvas>
</div>

<style>
	.chart-container {
		position: relative;
		height: 300px;
		width: 500px;
	}
</style>
